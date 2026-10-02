"""Download previews must stay separate from radio assets and regenerate safely."""
from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageDraw

import theme_lib


class DownloadPreviewPackageTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.theme = self.root / "theme-copperline"
        shutil.copytree(theme_lib.THEMES_ROOT / "theme-copperline", self.theme)
        self.preview = self.theme / "preview.png"
        self.preview.unlink(missing_ok=True)
        manifest = json.loads((self.theme / "ethos_lua_manifest.json").read_text(encoding="utf-8"))
        self.release = self.root / f"Copperline-v{manifest['version']}.zip"

    def build(self):
        with patch.object(theme_lib, "RELEASES_ROOT", self.root):
            theme_lib.write_release(self.theme, self.release)

    def runtime_bytes(self):
        return {path.name: path.read_bytes() for path in self.theme.iterdir()
                if path.name == "main.lua" or path.name.startswith(("toolbar-", "logo-"))}

    def test_archive_includes_decodable_preview_without_changing_radio_files(self):
        runtime_before = self.runtime_bytes()
        self.build()
        self.assertEqual(runtime_before, self.runtime_bytes())
        with zipfile.ZipFile(self.release) as archive:
            self.assertEqual(archive.read("preview.png"), self.preview.read_bytes())
            manifest = json.loads(archive.read("ethos_lua_manifest.json"))
            self.assertFalse(any(theme_lib.fnmatchcase("preview.png", selector.lower())
                                 for selector in manifest["files"]))
            self.assertNotIn(b"preview.png", archive.read("main.lua"))
        with Image.open(self.preview) as image:
            image.load()
            self.assertEqual(image.mode, "RGB")
            self.assertGreater(image.height, 400)

    def test_rebuild_is_reproducible_and_does_not_duplicate_preview_instructions(self):
        self.build()
        first = hashlib.sha256(self.release.read_bytes()).digest()
        self.build()
        self.assertEqual(first, hashlib.sha256(self.release.read_bytes()).digest())
        readme = (self.theme / "README.md").read_text(encoding="utf-8")
        self.assertEqual(readme.count("## Preview before installing"), 1)
        manifest = json.loads((self.theme / "ethos_lua_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["releaseNotes"]["content"].count(theme_lib.PREVIEW_RELEASE_NOTES), 1)

    def test_changed_header_refreshes_preview_instead_of_shipping_stale_image(self):
        self.build()
        before = self.preview.read_bytes()
        toolbar_path = self.theme / "toolbar-copperline.png"
        with Image.open(toolbar_path) as image:
            header = image.convert("RGB")
        ImageDraw.Draw(header).rectangle((0, 0, 160, 49), fill=(255, 0, 255))
        theme_lib.save_png(header, toolbar_path)
        self.build()
        self.assertNotEqual(before, self.preview.read_bytes())
        with zipfile.ZipFile(self.release) as archive:
            self.assertEqual(archive.read("preview.png"), self.preview.read_bytes())

    def test_overbroad_manifest_selector_is_rejected_before_packaging(self):
        path = self.theme / "ethos_lua_manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["files"].append("*.PNG")
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Desktop preview"):
            self.build()
        self.assertFalse(self.release.exists())


if __name__ == "__main__":
    unittest.main()
