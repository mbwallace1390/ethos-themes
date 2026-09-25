"""Catalog previews must show the real artwork for each supported radio width."""
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image, ImageChops, ImageDraw

from palette_quality import ROLES
import preview_lib


class PreviewHeaderTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.folder = self.root / "theme-example"
        self.folder.mkdir()
        colors = "\n".join(f"lcd.RGB(0x12, 0x23, 0x34), -- {role}"
                           for role in ROLES if role != "OVERLAY_COLOR")
        (self.folder / "main.lua").write_text(
            'name = "Example"\nroundButtons = false\nfocusStyle = "outline"\n' + colors,
            encoding="utf-8")
        self.large_path = self.folder / "toolbar-example.png"
        self.small_path = self.folder / "toolbar-example-x18.png"
        Image.new("RGB", (784, 50), (45, 60, 110)).save(self.large_path)
        small = Image.new("RGB", (464, 50), (20, 95, 40))
        # Deliberately different geometry and one-pixel detail cannot be reproduced
        # by scaling the large fixture into a 480px-radio illustration.
        draw = ImageDraw.Draw(small)
        draw.rectangle((67, 9, 87, 29), fill=(180, 20, 50))
        small.putpixel((132, 17), (251, 229, 91))
        small.save(self.small_path)

    def test_small_header_uses_its_native_asset_without_resizing_the_large_one(self):
        with patch.object(preview_lib, "THEMES_ROOT", self.root):
            theme = preview_lib.parse_theme("example")
        self.assertEqual(theme["toolbar_x18"], self.small_path)
        large = preview_lib.toolbar_preview(theme)
        small = preview_lib.toolbar_preview(theme, display_width=480)
        self.assertEqual(large.size, (784, 50))
        self.assertEqual(small.size, (464, 50))
        with Image.open(self.small_path) as source:
            self.assertEqual(small.tobytes(), source.convert("RGB").tobytes())
        self.assertEqual(small.getpixel((132, 17)), (251, 229, 91))

    def test_missing_x18_art_is_reported_instead_of_showing_a_substitute(self):
        self.small_path.unlink()
        with patch.object(preview_lib, "THEMES_ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "Incomplete native theme"):
                preview_lib.parse_theme("example")

    def test_industrial_cards_show_both_headers_and_keep_everything_inside_bounds(self):
        for slug in ("carbon", "hazard"):
            with self.subTest(theme=slug):
                theme = preview_lib.parse_theme(slug)
                background = Image.new("RGB", (640, 520), (137, 13, 121))
                canvas = background.copy()
                x, y = 31, 37
                preview_lib.draw_card(canvas, theme, x, y)
                large = preview_lib.toolbar_preview(theme)
                scaled_height = round(large.height * 512 / large.width)
                expected_large = large.resize((512, scaled_height), Image.Resampling.LANCZOS)
                self.assertEqual(canvas.crop((x + 20, y + 83, x + 532,
                                              y + 83 + scaled_height)).tobytes(),
                                 expected_large.tobytes())
                small = preview_lib.toolbar_preview(theme, display_width=480)
                # The X18 sample remains 464x50 and occupies its own lower row.
                self.assertEqual(canvas.crop((x + 44, y + 148, x + 508, y + 198)).tobytes(),
                                 small.tobytes())
                bounds = ImageChops.difference(canvas, background).getbbox()
                self.assertIsNotNone(bounds)
                self.assertGreaterEqual(bounds[0], x)
                self.assertGreaterEqual(bounds[1], y)
                self.assertLessEqual(bounds[2], x + preview_lib.CARD_WIDTH + 1)
                self.assertLessEqual(bounds[3], y + preview_lib.CARD_HEIGHT + 1)


if __name__ == "__main__":
    unittest.main()
