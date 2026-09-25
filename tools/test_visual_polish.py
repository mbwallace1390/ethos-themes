"""Check visible theme details and selected-control contrast at native sizes."""
from __future__ import annotations

import unittest

from PIL import Image, ImageDraw

import generate_cancer_awareness_themes as awareness
import generate_custom_art_themes as custom
from palette_quality import SURFACES, contrast_ratio, polish_palette


class VisualPolishTests(unittest.TestCase):
    def neon(self, width):
        theme = next(theme for theme in custom.THEMES if theme[1] == "neon-horizon")
        return theme, custom.make_toolbar(theme, width)

    def test_neon_sun_bands_stay_inside_its_oval(self):
        for width in (464, 784):
            with self.subTest(width=width):
                theme, image = self.neon(width)
                accent = custom.color(theme[-1][2])
                stripe = custom.mix(custom.color(theme[-1][8]), accent, .45)
                pixels = image.load()
                # Infer the visible sun's boundary from its pink outline. The
                # bands must not protrude beyond this silhouette at any row.
                outline = [(x, y) for y in range(41) for x in range(width)
                           if pixels[x, y] == accent]
                self.assertTrue(outline, "sun outline is missing")
                bounds = (min(x for x, _ in outline), min(y for _, y in outline),
                          max(x for x, _ in outline), max(y for _, y in outline))
                mask = Image.new("1", image.size)
                ImageDraw.Draw(mask).ellipse(bounds, fill=1)
                bands = [(x, y) for y in range(41) for x in range(width)
                         if pixels[x, y] == stripe]
                self.assertGreaterEqual(len({y for _, y in bands}), 4,
                                        "the striped sunset identity is missing")
                self.assertTrue(all(mask.getpixel(point) for point in bands),
                                "sun bands protrude outside the oval")

    def test_neon_perspective_floor_has_depth_and_clears_the_wordmark(self):
        for width in (464, 784):
            with self.subTest(width=width):
                _, image = self.neon(width)
                pixels = image.load()

                def cyan(x, y):
                    red, green, blue = pixels[x, y]
                    return green >= 70 and blue >= 85 and green > red * 1.5

                # A floor compressed into the last seven pixels looks like a
                # double underline. Require visible depth on both open flanks.
                for x in (width // 8, width * 7 // 8):
                    rows = [y for y in range(50) if cyan(x, y)]
                    self.assertGreaterEqual(len(rows), 4, "grid cross-lines are missing")
                    self.assertGreaterEqual(max(rows) - min(rows), 15,
                                            "perspective floor is too shallow")
                left = (width - 128) // 2
                self.assertFalse(any(cyan(x, y) for x in range(left, left + 128)
                                     for y in range(12, 40)),
                                 "bright perspective lines cross the wordmark")
                self.assertTrue(all(any(cyan(x, y) for y in range(41, 49))
                                    for x in range(width)),
                                "perspective floor is interrupted beneath the wordmark")

    def test_selected_outlines_and_highlight_text_remain_readable(self):
        royal = next(theme for theme in awareness.THEMES if theme[0] == "royal-blue-strong")
        desert = next(theme for theme in custom.THEMES if theme[1] == "desert-tactical")
        desert_colors = dict(zip(custom.ROLES, map(custom.color, desert[-1])))
        desert_colors.update(OVERLAY_COLOR=(0, 0, 0),
                             TOPLCD_BGCOLOR=desert_colors["PAGE_BGCOLOR"])
        royal_colors = awareness.palette(royal)
        royal_colors["OVERLAY_COLOR"] = (0, 0, 0)
        for slug, raw in ((royal[0], royal_colors),
                          (desert[1], desert_colors)):
            with self.subTest(theme=slug):
                colors = polish_palette(raw)
                for surface in SURFACES:
                    self.assertGreaterEqual(contrast_ratio(colors["HIGHLIGHT_COLOR"], colors[surface]),
                                            3.0, f"{slug}: selected outline disappears on {surface}")
                self.assertGreaterEqual(contrast_ratio(colors["HIGHLIGHT_COLOR"],
                                                      colors["HIGHLIGHT_CONTRASTING_COLOR"]), 4.5)


if __name__ == "__main__":
    unittest.main()
