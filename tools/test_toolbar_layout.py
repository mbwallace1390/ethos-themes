"""Keep shipped decoration and halo light outside the padded ETHOS wordmark area."""
from __future__ import annotations

import unittest

from PIL import Image, ImageDraw

from generate_ink_halo_theme import INK, PANEL, halo_background
from theme_lib import THEMES_ROOT, compose_toolbar_sides


# A 128px wordmark has 16px padding on each side. Keep this acceptance boundary
# independent of the generator constant so narrowing the clear area is detected.
CLEAR_WIDTH = 160
BAKED_TEXT_THEMES = {"theme-america250", "theme-ink-halo"}


class ToolbarLayoutTests(unittest.TestCase):
    def assert_plain_logo_area(self, image, label):
        image = image.convert("RGB")
        pixels = image.load()
        left = (image.width - CLEAR_WIDTH) // 2
        row_colors = []
        for y in range(8, 43):
            colors = {pixels[x, y] for x in range(left, left + CLEAR_WIDTH)}
            self.assertEqual(len(colors), 1,
                             f"{label}: decoration enters the logo area at row {y}")
            row_colors.append(pixels[left, y])
        # Uniform horizontal accent bands can pass the row check. A quiet base
        # gradient changes gradually; allow 3/255 for indexed-color quantization.
        for y, (before, after) in enumerate(zip(row_colors, row_colors[1:]), start=9):
            self.assertLessEqual(max(abs(a - b) for a, b in zip(before, after)), 3,
                                 f"{label}: an accent band crosses the logo area at row {y}")

    def test_every_separate_logo_theme_ships_a_clear_center_at_both_sizes(self):
        themes = [path.parent for path in sorted(THEMES_ROOT.glob("*/main.lua"))
                  if path.parent.name not in BAKED_TEXT_THEMES]
        self.assertEqual(len(themes), 66)
        for folder in themes:
            artwork = sorted(folder.glob("toolbar-*.png"))
            self.assertEqual(len(artwork), 2, folder.name)
            for path in artwork:
                with self.subTest(theme=folder.name, artwork=path.name):
                    with Image.open(path) as image:
                        expected = (464, 50) if path.stem.endswith("-x18") else (784, 50)
                        self.assertEqual(image.size, expected)
                        self.assert_plain_logo_area(image, path.name)

    def test_ink_halo_has_no_arc_or_glow_behind_its_baked_wordmark(self):
        # Check the layer before its intentional lettering is pasted onto it.
        for width in (784, 464):
            with self.subTest(width=width):
                background = halo_background(width)
                left = (width - CLEAR_WIDTH) // 2
                pixels = background.load()
                for y in range(8, 46):
                    expected = tuple(round(start + (end - start) * y / 100)
                                     for start, end in zip(INK, PANEL))
                    self.assertEqual({pixels[x, y] for x in range(left, left + CLEAR_WIDTH)},
                                     {expected}, f"halo/glow behind wordmark at row {y}")

    def test_compositor_renders_native_flanks_without_touching_the_clear_center(self):
        for width, flank_width in ((784, 312), (464, 152)):
            with self.subTest(width=width):
                base = Image.new("RGB", (width, 50))
                draw = ImageDraw.Draw(base)
                for y in range(50):
                    draw.line((0, y, width - 1, y), fill=(y, y + 10, y + 20))
                calls = []
                colors = ((215, 45, 31), (24, 177, 219))

                def render(panel_width, height, side):
                    calls.append((panel_width, height, side))
                    return Image.new("RGB", (panel_width, height), colors[side])

                result = compose_toolbar_sides(base, render)
                self.assertEqual(calls, [(flank_width, 50, 0), (flank_width, 50, 1)])
                area = (flank_width, 0, flank_width + CLEAR_WIDTH, 50)
                self.assertEqual(result.crop(area).tobytes(), base.crop(area).tobytes())
                self.assertEqual(result.getpixel((0, 25)), colors[0])
                self.assertEqual(result.getpixel((width - 1, 25)), colors[1])


if __name__ == "__main__":
    unittest.main()
