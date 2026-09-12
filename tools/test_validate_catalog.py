"""Regression checks for release completeness and ETHOS Suite install files."""

from __future__ import annotations

import json
import io
import struct
import tempfile
import unittest
import zipfile
import zlib
from contextlib import redirect_stdout
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
                "manifestVersion": 1,
                "name": "Example",
                "key": "example",
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
        self.root = Path(temporary.name)
        self.theme = self.root / "themes" / "theme-example"
        self.theme.mkdir(parents=True)
        (self.root / "releases").mkdir()
        (self.root / "README.md").write_text("# Example catalog\n", encoding="utf-8")
        (self.theme / "main.lua").write_text(
            'local version = system.getVersion()\nlocal width = version.lcdWidth\n'
            'return { key = "Example", name = "Example", '
            '"toolbar-example.png", "toolbar-example-x18.png" }\n', encoding="utf-8"
        )
        (self.theme / "README.md").write_text("Example\n", encoding="utf-8")
        for name, size in (("toolbar-example.png", (784, 50)),
                           ("toolbar-example-x18.png", (464, 50))):
            Image.new("P", size).save(self.theme / name)

    def problems(self, files: object, *, overrides: dict | None = None,
                 omit: tuple[str, ...] = ()) -> list[str]:
        manifest = {
            "manifestVersion": 1,
            "name": "Example", "folder": "theme-example", "key": "example",
            "version": "1.0.1", "files": files,
        }
        manifest.update(overrides or {})
        for field in omit:
            del manifest[field]
        (self.theme / "ethos_lua_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        return self.written_theme_problems()

    def written_theme_problems(self) -> list[str]:
        problems: list[str] = []
        validate_catalog.check_theme(self.theme, problems)
        return problems

    def catalog_result(self) -> tuple[int, str]:
        # A matching ZIP must not conceal invalid source files or metadata.
        with zipfile.ZipFile(self.root / "releases" / "Example-v1.0.1.zip", "w") as archive:
            for path in self.theme.iterdir():
                archive.write(path, path.name)
        output = io.StringIO()
        with patch.multiple(validate_catalog, ROOT=self.root,
                            THEMES_ROOT=self.root / "themes", RELEASES_ROOT=self.root / "releases"):
            with redirect_stdout(output):
                result = validate_catalog.main()
        return result, output.getvalue()

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

    def test_custom_logo_must_exist_and_be_installed(self) -> None:
        source = self.theme / "main.lua"
        source.write_text(source.read_text() + '\n-- optional bitmap: "logo-transparent.png"\n')
        problems = self.problems(["main.lua", "toolbar-*"])
        self.assertTrue(any("references missing image logo-transparent.png" in item for item in problems))
        Image.new("RGBA", (1, 1), (0, 0, 0, 0)).save(self.theme / "logo-transparent.png")
        self.assertTrue(any("does not install logo-transparent.png" in item
                            for item in self.problems(["main.lua", "toolbar-*"])))
        self.assertEqual(self.problems(["main.lua", "toolbar-*", "logo-transparent.png"]), [])

    def test_install_patterns_must_be_a_nonempty_string_list(self) -> None:
        for files in (None, [], "main.lua", [None], [""]):
            with self.subTest(files=files):
                self.assertTrue(any("manifest files" in item for item in self.problems(files)))

    def test_required_manifest_fields_cannot_be_missing_even_in_matching_zip(self) -> None:
        for field in ("manifestVersion", "name", "key", "version", "folder", "files"):
            with self.subTest(field=field):
                problems = self.problems(["main.lua", "toolbar-*"], omit=(field,))
                self.assertTrue(any(f"manifest {field}" in item for item in problems), problems)
        self.problems(["main.lua", "toolbar-*"], omit=("manifestVersion", "key"))
        result, output = self.catalog_result()
        self.assertEqual(result, 1, output)
        self.assertIn("manifest manifestVersion", output)
        self.assertIn("manifest key", output)

    def test_manifest_types_formats_and_limits_are_enforced(self) -> None:
        invalid = {
            "manifestVersion": (True, 1.0, "1", 2, None),
            "name": ([], "", "a" * 129),
            "key": ([], "", ":example", "a" * 129, "example/invalid"),
            "version": ([], 1, "1.2", "1.2.3-beta", "\uff11.2.3"),
            "folder": ([], "", "bad/folder", "-theme", "a" * 65),
        }
        for field, values in invalid.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    problems = self.problems(["main.lua", "toolbar-*"], overrides={field: value})
                    self.assertTrue(any(f"manifest {field}" in item for item in problems), problems)

    def test_manifest_optional_metadata_types_and_limits_are_enforced(self) -> None:
        for field, values in {
            "introduction": (12, "a" * 1025),
            "releaseNotes": ([], "a" * 32001, {"format": "html", "content": "Notes"},
                             {"format": "markdown", "content": 12}),
        }.items():
            for value in values:
                with self.subTest(field=field, value_type=type(value).__name__):
                    problems = self.problems(["main.lua", "toolbar-*"], overrides={field: value})
                    self.assertTrue(any(f"manifest {field}" in item for item in problems), problems)

    def test_manifest_paths_reject_unsafe_or_malformed_selectors(self) -> None:
        for selector in ("../file", "assets/../file", "..", "/file", "C:/file", "C:file",
                         "assets//file", "assets/", "assets\\file", "//server/file"):
            with self.subTest(selector=selector):
                problems = self.problems(["main.lua", "toolbar-*", selector])
                self.assertTrue(any("files selector" in item for item in problems), problems)

    def test_documented_globs_case_insensitivity_and_valid_boundaries_are_accepted(self) -> None:
        self.assertEqual(self.problems(
            ["MAIN.LUA", "TOOLBAR-*", "i18n/*", "assets/**"],
            overrides={"key": "A" + ".a_:-0" * 21 + "Z", "version": "01.02.003",
                       "introduction": "a" * 1024,
                       "releaseNotes": {"format": "text", "content": "a" * 32000}},
        ), [])

    def test_manifest_maximum_name_key_and_folder_lengths_are_accepted(self) -> None:
        self.assertEqual(validate_catalog.manifest_errors({
            "manifestVersion": 1, "name": "N" * 128, "key": "K" * 128,
            "version": "1.2.3", "folder": "F" * 64, "files": ["main.lua"],
            "releaseNotes": "Release notes",
        }), [])

    def test_nonobject_and_non_utf8_manifests_report_errors_without_crashing(self) -> None:
        path = self.theme / "ethos_lua_manifest.json"
        for value in ([], None, True, "manifest"):
            with self.subTest(value=value):
                path.write_text(json.dumps(value), encoding="utf-8")
                self.assertTrue(any("manifest must be a JSON object" in item
                                    for item in self.written_theme_problems()))
                self.assertIsNone(validate_catalog.current_version(self.theme))
                result, output = self.catalog_result()
                self.assertEqual(result, 1, output)
        path.write_bytes(b"\xff")
        self.assertTrue(any("unreadable manifest" in item for item in self.written_theme_problems()))
        self.assertIsNone(validate_catalog.current_version(self.theme))
        result, output = self.catalog_result()
        self.assertEqual(result, 1, output)

    def test_png_pixel_stream_must_decode_even_with_valid_chunk_checksums(self) -> None:
        path = self.theme / "toolbar-example.png"
        data = bytearray(path.read_bytes())
        offset = 8
        while offset < len(data):
            length = struct.unpack(">I", data[offset:offset + 4])[0]
            if data[offset + 4:offset + 8] == b"IDAT":
                data[offset + 8] = 0  # Invalid zlib header, with a valid PNG CRC.
                checksum = zlib.crc32(data[offset + 4:offset + 8 + length]) & 0xffffffff
                data[offset + 8 + length:offset + 12 + length] = struct.pack(">I", checksum)
                break
            offset += length + 12
        else:
            self.fail("Fixture has no IDAT chunk")
        path.write_bytes(data)
        with Image.open(path) as image:
            image.verify()  # Metadata and chunk integrity alone still pass.
        with self.assertRaises(OSError):
            with Image.open(path) as image:
                image.load()
        problems = self.problems(["main.lua", "toolbar-*"])
        self.assertTrue(any("unreadable image toolbar-example.png" in item for item in problems), problems)
        result, output = self.catalog_result()
        self.assertEqual(result, 1, output)

    def test_png_invalid_chunk_checksum_is_reported(self) -> None:
        path = self.theme / "toolbar-example.png"
        data = bytearray(path.read_bytes())
        offset = 8
        while offset < len(data):
            length = struct.unpack(">I", data[offset:offset + 4])[0]
            if data[offset + 4:offset + 8] == b"IDAT":
                data[offset + 8 + length] ^= 1
                break
            offset += length + 12
        else:
            self.fail("Fixture has no IDAT chunk")
        path.write_bytes(data)
        with Image.open(path) as image:
            image.load()  # Pillow decoding alone ignores this IDAT CRC error.
        problems = self.problems(["main.lua", "toolbar-*"])
        self.assertTrue(any("unreadable image toolbar-example.png" in item for item in problems), problems)

    def test_invalid_optional_logo_and_manifest_both_report_in_one_pass(self) -> None:
        source = self.theme / "main.lua"
        source.write_text(source.read_text() + '\n-- optional bitmap: "logo-transparent.png"\n')
        (self.theme / "logo-transparent.png").write_bytes(b"not a PNG")
        problems = self.problems(["main.lua", "toolbar-*", "logo-transparent.png"],
                                 overrides={"key": []})
        self.assertTrue(any("unreadable image logo-transparent.png" in item for item in problems), problems)
        self.assertTrue(any("manifest key" in item for item in problems), problems)
        result, output = self.catalog_result()
        self.assertEqual(result, 1, output)
        self.assertIn("unreadable image logo-transparent.png", output)
        self.assertIn("manifest key", output)


if __name__ == "__main__":
    unittest.main()
