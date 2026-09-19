"""Regression coverage for adding logos to hand-maintained legacy themes."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from palette_quality import ROLES
from theme_lib import INIT_GUARD_LUA, add_toolbar_logo


class LogoGenerationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name) / "theme-example"
        self.folder.mkdir()
        rows = [f"            lcd.RGB(0xF4, 0xF7, 0xFC), -- {role}"
                for role in ROLES if role != "OVERLAY_COLOR"]
        self.source = (
            "local function init()\n" + INIT_GUARD_LUA
            + "    system.registerTheme({\n        colors = {\n"
            + "\n".join(rows) + "\n        },\n"
            + '        --toolbarLogo = "none",\n'
            + '        toolbarBackground = loadToolbar("toolbar-example.png", "toolbar-example-x18.png"),\n'
            + "    })\nend\nreturn { init = init }\n"
        )
        (self.folder / "main.lua").write_text(self.source, encoding="utf-8")
        (self.folder / "ethos_lua_manifest.json").write_text(json.dumps({
            "files": ["main.lua", "toolbar-*"],
            "releaseNotes": {"format": "markdown", "content": "Existing release."},
        }), encoding="utf-8")
        # Classic Blue has numbered instructions rather than a generated marker.
        (self.folder / "README.md").write_text(
            "# Example\n\n## Installation\n\n1. Copy the theme folder.\n", encoding="utf-8")

    def test_commented_legacy_logo_does_not_block_real_bitmap(self):
        logo_name = add_toolbar_logo(self.folder, "example")
        source = (self.folder / "main.lua").read_text(encoding="utf-8")
        self.assertNotIn('--toolbarLogo = "none"', source)
        self.assertEqual(source.count("        toolbarLogo = toolbarLogo,"), 1)
        self.assertIn(f'pcall(lcd.loadBitmap, "{logo_name}")', source)
        with Image.open(self.folder / logo_name) as logo:
            logo.load()
            self.assertEqual((logo.size, logo.mode), ((128, 26), "RGBA"))
        manifest = json.loads((self.folder / "ethos_lua_manifest.json").read_text(encoding="utf-8"))
        self.assertIn(logo_name, manifest["files"])
        readme = (self.folder / "README.md").read_text(encoding="utf-8")
        self.assertIn("Palette-matched ETHOS header logo", readme)
        self.assertIn("1. Copy the theme folder.", readme)

    def test_existing_active_override_is_rejected_before_writes(self):
        path = self.folder / "main.lua"
        path.write_text(self.source.replace('--toolbarLogo = "none",',
                                            "toolbarLogo = existingBitmap,"), encoding="utf-8")
        before = {item.name: item.read_bytes() for item in self.folder.iterdir()}
        with self.assertRaisesRegex(ValueError, "already configured"):
            add_toolbar_logo(self.folder, "example")
        self.assertEqual(before, {item.name: item.read_bytes() for item in self.folder.iterdir()})


if __name__ == "__main__":
    unittest.main()
