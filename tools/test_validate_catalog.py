"""Regression checks for release completeness and ETHOS Suite install files."""

from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from PIL import Image

import validate_catalog


class ReleaseValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.themes = self.root / "themes"
        self.releases = self.root / "releases"
        self.theme = self.themes / "theme-example"
        self.theme.mkdir(parents=True)
        self.releases.mkdir()
        self.files = {
            "main.lua": b"return { init = function() end }\n",
            "README.md": b"Example theme\n",
            "ethos_lua_manifest.json": json.dumps({
                "folder": "theme-example",
                "version": "1.1.0",
                "files": ["main.lua", "toolbar-*"],
            }).encode(),
            "toolbar-example.png": b"large artwork",
            "toolbar-example-x18.png": b"small artwork",
        }
        for name, content in self.files.items():
            (self.theme / name).write_bytes(content)
        patches = patch.multiple(
            validate_catalog, THEMES_ROOT=self.themes, RELEASES_ROOT=self.releases
        )
        patches.start()
        self.addCleanup(patches.stop)

    def archive(self, version: str = "1.1.0", *, omit: str | None = None,
                extra: dict[str, bytes] | None = None, nested: bool = False) -> None:
        prefix = "theme-example/" if nested else ""
        with zipfile.ZipFile(self.releases / f"Example-v{version}.zip", "w") as archive:
            for name, content in self.files.items():
                if name != omit:
                    if name == "ethos_lua_manifest.json":
                        manifest = json.loads(content)
                        manifest["version"] = version
                        content = json.dumps(manifest).encode()
                    archive.writestr(f"{prefix}{name}", content)
            for name, content in (extra or {}).items():
                archive.writestr(f"{prefix}{name}", content)

    def problems(self) -> list[str]:
        problems: list[str] = []
        validate_catalog.check_releases(problems)
        return problems

    def test_complete_current_archive_accepts_frozen_older_release(self) -> None:
        self.archive("1.0.0", omit="main.lua", nested=True)
        self.archive()
        self.assertEqual(self.problems(), [])

    def test_only_superseded_archive_does_not_count_as_current(self) -> None:
        self.archive("1.0.0", nested=True)
        self.assertTrue(any("no current release ZIP" in item for item in self.problems()))

    def test_current_archive_must_include_every_theme_file(self) -> None:
        for omitted in self.files:
            with self.subTest(omitted=omitted):
                self.archive(omit=omitted)
                self.assertTrue(any(
                    f"missing {omitted}" in item for item in self.problems()
                ))

    def test_nested_current_archive_is_not_a_suite_install_package(self) -> None:
        self.archive(nested=True)
        self.assertTrue(any("missing ethos_lua_manifest.json at ZIP root" in item
                            for item in self.problems()))

    def test_compiled_lua_cannot_ship_even_if_present_on_disk(self) -> None:
        (self.theme / "main.luac").write_bytes(b"old bytecode")
        self.archive(extra={"main.luac": b"old bytecode"})
        self.assertTrue(any("main.luac" in item for item in self.problems()))

    def test_unexpected_archive_file_is_rejected(self) -> None:
        self.archive(extra={"old-toolbar.png": b"outdated artwork"})
        self.assertTrue(any("old-toolbar.png" in item for item in self.problems()))

    def test_stale_archive_bytes_are_rejected(self) -> None:
        self.archive()
        (self.theme / "main.lua").write_bytes(b"updated Lua\n")
        self.assertTrue(any("main.lua is stale" in item for item in self.problems()))


class ManifestInstallTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.theme = Path(temporary.name) / "theme-example"
        self.theme.mkdir()
        (self.theme / "main.lua").write_text(
            'local version = system.getVersion()\nlocal width = version.lcdWidth\n'
            'return { key = "Example", name = "Example", '
            '"toolbar-example.png", "toolbar-example-x18.png" }\n', encoding="utf-8"
        )
        (self.theme / "README.md").write_text("Example\n", encoding="utf-8")
        for name, size in (("toolbar-example.png", (784, 50)),
                           ("toolbar-example-x18.png", (464, 50))):
            Image.new("P", size).save(self.theme / name)

    def problems(self, files: object) -> list[str]:
        (self.theme / "ethos_lua_manifest.json").write_text(json.dumps({
            "name": "Example", "folder": "theme-example", "key": "example",
            "version": "1.0.1", "files": files,
        }), encoding="utf-8")
        problems: list[str] = []
        validate_catalog.check_theme(self.theme, problems)
        return problems

    def test_valid_install_patterns_cover_lua_and_both_toolbars(self) -> None:
        self.assertEqual(self.problems(["main.lua", "toolbar-*"]), [])

    def test_install_patterns_cannot_omit_lua_or_a_toolbar(self) -> None:
        for files, missing in ((["toolbar-*"], "main.lua"),
                               (["main.lua", "toolbar-example.png"], "toolbar-example-x18.png"),
                               (["main.lua", "toolbar-example-x18.png"], "toolbar-example.png")):
            with self.subTest(files=files):
                self.assertTrue(any(
                    f"does not install {missing}" in item for item in self.problems(files)
                ))

    def test_install_patterns_cannot_include_compiled_lua(self) -> None:
        for files in (["main.lua", "toolbar-*", "main.luac"], ["*"]):
            with self.subTest(files=files):
                self.assertTrue(any("main.luac" in item for item in self.problems(files)))

    def test_install_patterns_must_be_a_nonempty_string_list(self) -> None:
        for files in (None, [], "main.lua", [None], [""]):
            with self.subTest(files=files):
                self.assertTrue(any("manifest files" in item for item in self.problems(files)))


if __name__ == "__main__":
    unittest.main()
