"""Keep toolbar materials continuous and bright accents clear of ETHOS lettering."""
from __future__ import annotations

import unittest

from PIL import Image

from generate_ink_halo_theme import INK, PANEL, halo_background
from theme_lib import THEMES_ROOT


RAIL_THEMES = (
    "amber-instrument", "phosphor-green", "ice-instrument",
    "soft-lavender", "soft-mint", "soft-coral", "soft-sky",
    "oled-blue", "oled-red", "oled-green", "oled-white",
    "daylight-blue", "daylight-orange", "daylight-green",
    "carbon", "gunmetal", "titanium", "violet-circuit", "blue-vector",
    "ember-signal", "neon-fusion", "rfblue-pro", "rf-violet-pro",
    "rf-emerald-pro", "rf-ember-pro", "rf-magenta-pro", "rf-cyan-pro",
    "rf-crimson-pro", "rf-gold-pro", "rf-teal-pro", "rf-lime-pro",
)


class ToolbarLayoutTests(unittest.TestCase):
    def artwork(self, slug):
        paths = sorted((THEMES_ROOT / f"theme-{slug}").glob("toolbar-*.png"))
        self.assertEqual(len(paths), 2, slug)
        for path in paths:
            with Image.open(path) as image:
                expected = (464, 50) if path.stem.endswith("-x18") else (784, 50)
                self.assertEqual(image.size, expected)
                yield path.name, image.convert("RGB")

    def assert_visible_center_texture(self, image, label):
        pixels = image.load()
        left = (image.width - 128) // 2
        visible_rows = 0
        for y in range(13, 40):
            colors = {pixels[x, y] for x in range(left, left + 128)}
            visible_rows += len(colors) > 1
            # Subdued materials may remain under transparent lettering. Avoid
            # replacing that detail with either a flat fill or a bright flare.
            variation = max(max(color[channel] for color in colors)
                            - min(color[channel] for color in colors) for channel in range(3))
            self.assertLessEqual(variation, 176, f"{label}: texture overwhelms the lettering")
        # Dot screens have intentional empty rows. Require detail throughout the
        # region without mistaking their normal spacing for a rectangular patch.
        self.assertGreaterEqual(visible_rows, 9, f"{label}: the material has a blank center patch")

    def test_carbon_weave_glass_and_dots_remain_visible_under_the_logo(self):
        for slug in ("carbon", "loom", "mosaic", "halftone"):
            for label, image in self.artwork(slug):
                with self.subTest(artwork=label):
                    self.assert_visible_center_texture(image, label)

    def test_brushed_material_runs_across_the_full_toolbar(self):
        for slug in ("gunmetal", "titanium"):
            for label, image in self.artwork(slug):
                with self.subTest(artwork=label):
                    pixels = image.load()
                    for y in (12, 18, 24, 30):
                        self.assertEqual(len({pixels[x, y] for x in range(image.width)}), 1,
                                         f"{label}: brushed grain stops beside the logo")

    def assert_continuous_lower_rail(self, image, label):
        pixels = image.load()
        # A visible rail must cross every column below the letters, including
        # the middle. Compare with the local material above it, allowing texture.
        has_rail = any(all(max(abs(a - b) for a, b in zip(pixels[x, y], pixels[x, 30])) >= 24
                           for x in range(image.width)) for y in range(41, 49))
        self.assertTrue(has_rail, f"{label}: the lower accent rail is missing or interrupted")

    def test_standalone_and_pro_accent_rails_continue_beneath_the_letters(self):
        for slug in RAIL_THEMES:
            for label, image in self.artwork(slug):
                with self.subTest(artwork=label):
                    self.assert_continuous_lower_rail(image, label)

    def test_hazard_stripes_continue_through_the_middle(self):
        for label, image in self.artwork("hazard"):
            with self.subTest(artwork=label):
                pixels = image.load()
                # Every short section of the lower strip needs dark and yellow
                # paint. The former 160px blank gap fails several such sections.
                for left in range(0, image.width - 47, 24):
                    colors = {pixels[x, 44] for x in range(left, left + 48)}
                    self.assertGreater(len(colors), 1, f"{label}: missing stripes near x={left}")
                    self.assertGreater(max(max(c) for c in colors) - min(max(c) for c in colors), 100,
                                       f"{label}: faded or missing hazard band near x={left}")

    def assert_connected_lower_fissure(self, image, label):
        pixels = image.load()
        # Include the visible glow and dim sparks along the crack. Their channel
        # values exceed 80; the underlying near-black rock remains below 25.
        remaining = {(x, y) for y in range(15, 49) for x in range(image.width)
                     if max(pixels[x, y]) >= 80}
        spanning = None
        # Trace real neighboring pixels: sparks cannot hide a missing section
        # of fissure, and a disconnected left/right pair cannot count as a line.
        while remaining and spanning is None:
            start = remaining.pop()
            component, pending = {start}, [start]
            while pending:
                x, y = pending.pop()
                for dx, dy in ((-1, -1), (0, -1), (1, -1), (-1, 0),
                               (1, 0), (-1, 1), (0, 1), (1, 1)):
                    neighbor = (x + dx, y + dy)
                    if neighbor in remaining:
                        remaining.remove(neighbor)
                        component.add(neighbor)
                        pending.append(neighbor)
            columns = {x for x, _ in component}
            if 0 in columns and image.width - 1 in columns:
                spanning = component
        self.assertIsNotNone(spanning, f"{label}: fissure does not connect both toolbar edges")
        left = (image.width - 128) // 2
        self.assertTrue(all(y >= 41 for x, y in spanning if left <= x < left + 128),
                        f"{label}: the fissure crosses the lettering")
        self.assertLess(max(max(pixels[x, y]) for x in range(left, left + 128)
                            for y in range(13, 40)), 80,
                        f"{label}: bright fissure glow or sparks cross the lettering")

    def test_molten_fissures_are_connected_and_bow_below_the_wordmark(self):
        for slug in ("molten-ember", "molten-sulfur", "molten-verdigris"):
            for label, image in self.artwork(slug):
                with self.subTest(artwork=label):
                    self.assert_connected_lower_fissure(image, label)

    def test_ink_halo_has_no_arc_or_glow_behind_its_baked_wordmark(self):
        # Check the layer before its intentional lettering is pasted onto it.
        for width in (784, 464):
            with self.subTest(width=width):
                background = halo_background(width)
                left = (width - 160) // 2
                pixels = background.load()
                for y in range(8, 46):
                    expected = tuple(round(start + (end - start) * y / 100)
                                     for start, end in zip(INK, PANEL))
                    self.assertEqual({pixels[x, y] for x in range(left, left + 160)},
                                     {expected}, f"halo/glow behind wordmark at row {y}")


if __name__ == "__main__":
    unittest.main()
