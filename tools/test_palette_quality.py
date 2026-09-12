"""Contrast-policy regressions using independent color and Lua fixtures."""

from __future__ import annotations

import unittest

from palette_quality import contrast_ratio, polish_lua_source, polish_palette


ROLES = (
    "PRIMARY_COLOR", "SECONDARY_BGCOLOR", "HIGHLIGHT_COLOR",
    "HIGHLIGHT_CONTRASTING_COLOR", "DISABLE_COLOR", "PRIMARY_BGCOLOR",
    "OVERLAY_COLOR", "SECONDARY_COLOR", "SAFE_COLOR", "PAGE_BGCOLOR",
    "ERROR_COLOR", "ACTIVE_COLOR", "INACTIVE_COLOR",
    "BUTTON_BORDER_ACTIVE_COLOR", "BUTTON_BORDER_COLOR", "WARNING_COLOR",
    "SAFE_CONTRASTING_COLOR", "TOPLCD_BGCOLOR",
)
SURFACES = ("PRIMARY_BGCOLOR", "SECONDARY_BGCOLOR", "PAGE_BGCOLOR")
FOREGROUNDS = {
    "PRIMARY_COLOR", "SECONDARY_COLOR", "HIGHLIGHT_CONTRASTING_COLOR",
    "SAFE_CONTRASTING_COLOR", "ACTIVE_COLOR", "INACTIVE_COLOR", "DISABLE_COLOR",
}

# Original Daylight Orange v1.1.0 palette. Its selected-control text is
# approximately 2.94:1, and its safe-control text is approximately 3.77:1.
DAYLIGHT_ORANGE = dict(zip(ROLES, (
    (0x12, 0x18, 0x1E), (0xE8, 0xE1, 0xDB), (0xE8, 0x6E, 0x00),
    (0xF5, 0xF7, 0xFA), (0x91, 0x99, 0xA1), (0xFF, 0xFF, 0xFF),
    (0, 0, 0), (0x46, 0x46, 0x46), (0x14, 0x91, 0x50),
    (0xF5, 0xF2, 0xF1), (0xCC, 0x28, 0x32), (0xE8, 0x6E, 0x00),
    (0x69, 0x77, 0x84), (0xE8, 0x6E, 0x00), (0xBF, 0xBD, 0xBC),
    (0xBE, 0x73, 0x00), (0xF5, 0xF7, 0xFA), (0xF5, 0xF2, 0xF1),
)))


def lua_fixture(palette: dict[str, tuple[int, int, int]]) -> str:
    lines = []
    for role in ROLES:
        rgb = palette[role]
        expression = "COLOR_BLACK" if role == "OVERLAY_COLOR" else (
            "lcd.RGB(" + ", ".join(f"0x{channel:02X}" for channel in rgb) + ")"
        )
        lines.append(f"            {expression}, -- {role}")
    return (
        "-- Preserve header and unrelated RGB calls exactly.\n"
        "local accent = lcd.RGB(0x01, 0x02, 0x03)\n"
        "local function init()\n"
        "    system.registerTheme({\n"
        '        key = "DayOrg", name = "Daylight Orange",\n'
        "        colors = {\n" + "\n".join(lines) + "\n        },\n"
        '        toolbarBackground = loadToolbar("large.png", "small.png"),\n'
        "    })\n"
        "end\nreturn { init = init }\n"
    )


class ContrastRatioTests(unittest.TestCase):
    def test_black_white_and_identical_colors(self) -> None:
        self.assertAlmostEqual(contrast_ratio((0, 0, 0), (255, 255, 255)), 21.0)
        self.assertEqual(contrast_ratio((37, 105, 219), (37, 105, 219)), 1.0)
        self.assertEqual(
            contrast_ratio((20, 100, 180), (235, 221, 205)),
            contrast_ratio((235, 221, 205), (20, 100, 180)),
        )

    def test_near_threshold_values_are_not_rounded_into_a_pass(self) -> None:
        self.assertLess(contrast_ratio((119, 119, 119), (255, 255, 255)), 4.5)
        self.assertGreater(contrast_ratio((118, 118, 118), (255, 255, 255)), 4.5)


class PalettePolishTests(unittest.TestCase):
    def assert_targets(self, palette: dict[str, tuple[int, int, int]]) -> None:
        for foreground in ("PRIMARY_COLOR", "SECONDARY_COLOR", "ACTIVE_COLOR", "INACTIVE_COLOR"):
            for background in SURFACES:
                with self.subTest(foreground=foreground, background=background):
                    self.assertGreaterEqual(contrast_ratio(palette[foreground], palette[background]), 4.5)
        for background in SURFACES:
            self.assertGreaterEqual(contrast_ratio(palette["DISABLE_COLOR"], palette[background]), 3.0)
        for foreground, background in (
            ("HIGHLIGHT_CONTRASTING_COLOR", "HIGHLIGHT_COLOR"),
            ("SAFE_CONTRASTING_COLOR", "SAFE_COLOR"),
        ):
            self.assertGreaterEqual(contrast_ratio(palette[foreground], palette[background]), 4.5)

    def test_real_daylight_orange_failures_are_fixed_without_mutating_input(self) -> None:
        original = DAYLIGHT_ORANGE.copy()
        self.assertLess(contrast_ratio(
            original["HIGHLIGHT_CONTRASTING_COLOR"], original["HIGHLIGHT_COLOR"]
        ), 3.0)
        result = polish_palette(original)
        self.assert_targets(result)
        self.assertEqual(original, DAYLIGHT_ORANGE)
        self.assertNotEqual(result["HIGHLIGHT_CONTRASTING_COLOR"], original["HIGHLIGHT_CONTRASTING_COLOR"])

    def test_brand_background_and_already_readable_foregrounds_are_preserved(self) -> None:
        result = polish_palette(DAYLIGHT_ORANGE.copy())
        for role in ROLES:
            if role not in FOREGROUNDS or role in ("PRIMARY_COLOR", "SECONDARY_COLOR"):
                with self.subTest(role=role):
                    self.assertEqual(result[role], DAYLIGHT_ORANGE[role])

    def test_already_good_palette_is_unchanged(self) -> None:
        palette = {role: (155, 155, 155) for role in ROLES}
        for role in SURFACES:
            palette[role] = (12, 12, 12)
        palette["HIGHLIGHT_CONTRASTING_COLOR"] = (0, 0, 0)
        palette["SAFE_CONTRASTING_COLOR"] = (0, 0, 0)
        palette["OVERLAY_COLOR"] = (0, 0, 0)
        self.assert_targets(palette)
        self.assertEqual(polish_palette(palette.copy()), palette)

    def test_repeated_polishing_is_idempotent(self) -> None:
        first = polish_palette(DAYLIGHT_ORANGE.copy())
        self.assertEqual(polish_palette(first.copy()), first)

    def test_near_threshold_text_gets_only_the_needed_one_step_adjustment(self) -> None:
        palette = DAYLIGHT_ORANGE.copy()
        for role in SURFACES:
            palette[role] = (255, 255, 255)
        palette["PRIMARY_COLOR"] = (119, 119, 119)
        result = polish_palette(palette)
        self.assertEqual(result["PRIMARY_COLOR"], (118, 118, 118))


class LuaPalettePolishTests(unittest.TestCase):
    def test_changes_are_confined_to_color_literals(self) -> None:
        source = lua_fixture(DAYLIGHT_ORANGE)
        result = polish_lua_source(source)
        self.assertNotEqual(result, source)
        self.assertEqual(source.split("        colors = {", 1)[0],
                         result.split("        colors = {", 1)[0])
        self.assertEqual(source.split("        },", 1)[1],
                         result.split("        },", 1)[1])
        self.assertIn("COLOR_BLACK, -- OVERLAY_COLOR", result)
        self.assertEqual(polish_lua_source(result), result)

    def test_missing_duplicate_reordered_and_computed_roles_are_rejected(self) -> None:
        source = lua_fixture(DAYLIGHT_ORANGE)
        first = "            lcd.RGB(0x12, 0x18, 0x1E), -- PRIMARY_COLOR\n"
        second = "            lcd.RGB(0xE8, 0xE1, 0xDB), -- SECONDARY_BGCOLOR\n"
        malformed = {
            "missing": source.replace(first, ""),
            "duplicate": source.replace("-- SECONDARY_BGCOLOR", "-- PRIMARY_COLOR"),
            "reordered": source.replace(first + second, second + first),
            "computed": source.replace("lcd.RGB(0x12, 0x18, 0x1E)", "calculateColor()"),
            "computed channel": source.replace("lcd.RGB(0x12, 0x18, 0x1E)", "lcd.RGB(18 + 0, 24, 30)"),
            "extra expression": source.replace("        colors = {\n", "        colors = {\n            calculateColor(),\n"),
            "out of range": source.replace("lcd.RGB(0x12, 0x18, 0x1E)", "lcd.RGB(256, 24, 30)"),
            "computed table": source.replace("colors = {", "colors = calculateColors {"),
        }
        for problem, candidate in malformed.items():
            with self.subTest(problem=problem):
                with self.assertRaises(ValueError):
                    polish_lua_source(candidate)


if __name__ == "__main__":
    unittest.main()
