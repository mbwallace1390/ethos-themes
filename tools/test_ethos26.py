"""Execute the catalog in Lua with the documented ETHOS 26.1.2 API surface.

These are API-stub checks, not firmware simulator or radio acceptance tests.
Requires development-only Pillow and lupa; no dependency is shipped to radios.
"""

from __future__ import annotations

import json
import re
import unittest
import zipfile

from lupa.lua52 import LuaRuntime as Lua52
from lupa.lua54 import LuaRuntime as Lua54

from theme_lib import RELEASES_ROOT, THEMES_ROOT, THEME_VERSION
from palette_quality import TARGETS, contrast_ratio

# Positional order from FrSky's theme-dracula/main.lua at release tag 26.1.2.
ROLES = (
    "PRIMARY_COLOR", "SECONDARY_BGCOLOR", "HIGHLIGHT_COLOR",
    "HIGHLIGHT_CONTRASTING_COLOR", "DISABLE_COLOR", "PRIMARY_BGCOLOR",
    "OVERLAY_COLOR", "SECONDARY_COLOR", "SAFE_COLOR", "PAGE_BGCOLOR",
    "ERROR_COLOR", "ACTIVE_COLOR", "INACTIVE_COLOR",
    "BUTTON_BORDER_ACTIVE_COLOR", "BUTTON_BORDER_COLOR", "WARNING_COLOR",
    "SAFE_CONTRASTING_COLOR", "TOPLCD_BGCOLOR",
)
THEMES = sorted(THEMES_ROOT.glob("*/main.lua"))
RUNTIMES = (Lua52, Lua54)

STUB = r'''
local function unexpected(_, name)
    error("Undocumented API access: " .. tostring(name))
end
registered = false
registrations = 0
bitmapCalls = 0
COLOR_BLACK = 0
system = setmetatable({
    getVersion = function() return testVersion end,
    registerTheme = function(theme)
        registrations = registrations + 1
        registered = theme
    end,
}, {__index = unexpected})
lcd = setmetatable({
    RGB = function(r, g, b)
        assert(type(r) == "number" and r >= 0 and r <= 255)
        assert(type(g) == "number" and g >= 0 and g <= 255)
        assert(type(b) == "number" and b >= 0 and b <= 255)
        return r * 65536 + g * 256 + b
    end,
    loadBitmap = function(path, lazy)
        assert(type(path) == "string")
        assert(lazy == nil or lazy == true, "Do not force eager bitmap loading")
        bitmapCalls = bitmapCalls + 1
        if bitmapMode == "error" then error("Bitmap initialization failed") end
        if bitmapMode == "nil" then return nil end
        return {path = path}
    end,
}, {__index = unexpected})
-- Existing API state is owned by the stub; theme code must not add globals.
setmetatable(_G, {__newindex = function(_, name)
    error("Theme wrote a global: " .. tostring(name))
end})
'''


def execute(source, runtime=Lua54, width=800, bitmap_mode="ok", supported=True):
    lua = runtime(unpack_returned_tuples=True)
    state = lua.globals()
    state.testVersion = lua.table_from({"major": 26, "minor": 1, "revision": 2})
    if width is not None:
        state.testVersion.lcdWidth = width
    state.bitmapMode = bitmap_mode
    lua.execute(STUB)
    if not supported:
        # Older firmware lacks registerTheme. Prove init exits before any LCD
        # calls even when none of the theme-specific API is available.
        lua.execute('system = {}; lcd = setmetatable({}, {__index = function() error("LCD called on unsupported firmware") end})')
    module = lua.execute(source)
    assert set(module.keys()) == {"init"}, "Themes must not register background tasks"
    module.init()
    return state


class Ethos26Tests(unittest.TestCase):
    def test_catalog_foregrounds_meet_readability_targets(self):
        # Validate the actual Lua values, not just the palette generator's inputs.
        for path in THEMES:
            with self.subTest(theme=path.parent.name):
                state = execute(path.read_text(encoding="utf-8"))
                colors = {}
                for index, role in enumerate(ROLES, 1):
                    value = int(state.registered.colors[index])
                    colors[role] = (value // 65536, value // 256 % 256, value % 256)
                for role, (target, surfaces) in TARGETS.items():
                    for surface in surfaces:
                        self.assertGreaterEqual(contrast_ratio(colors[role], colors[surface]), target,
                                                f"{path.parent.name}: {role} on {surface}")

    def test_catalog_registration_and_display_sizes(self):
        self.assertEqual(len(THEMES), 67)
        allowed = {"key", "name", "roundButtons", "focusStyle", "colors", "toolbarBackground"}
        for runtime in RUNTIMES:
            for path in THEMES:
                manifest = json.loads(path.with_name("ethos_lua_manifest.json").read_text())
                source = path.read_text(encoding="utf-8")
                roles = re.findall(r",\s*--\s*([A-Z_]+)", source)
                self.assertEqual(tuple(roles), ROLES, str(path))
                for width in (480, 800):
                    with self.subTest(lua=runtime.__module__, theme=path.parent.name, width=width):
                        state = execute(source, runtime, width)
                        theme = state.registered
                        self.assertEqual(state.registrations, 1)
                        self.assertEqual(set(theme.keys()), allowed)
                        self.assertEqual(theme.name, manifest["name"])
                        self.assertTrue(1 <= len(theme.key) <= 7)
                        self.assertIsInstance(theme.roundButtons, bool)
                        self.assertIn(theme.focusStyle, ("invert", "outline", "color"))
                        self.assertEqual(set(theme.colors.keys()), set(range(1, 19)))
                        self.assertTrue(all(isinstance(c, (int, float)) for c in theme.colors.values()))
                        self.assertEqual(state.bitmapCalls, 1)
                        art = theme.toolbarBackground.path
                        self.assertEqual(art.endswith("-x18.png"), width == 480)
                        self.assertTrue(path.with_name(art).is_file())

    def test_unknown_display_width_uses_large_art(self):
        for path in THEMES:
            for width in (None, "480"):
                with self.subTest(theme=path.parent.name, width=width):
                    state = execute(path.read_text(), width=width)
                    self.assertFalse(state.registered.toolbarBackground.path.endswith("-x18.png"))

    def test_bitmap_initialization_failure_keeps_palette(self):
        for runtime in RUNTIMES:
            for path in THEMES:
                for mode in ("error", "nil"):
                    with self.subTest(lua=runtime.__module__, theme=path.parent.name, mode=mode):
                        state = execute(path.read_text(), runtime, bitmap_mode=mode)
                        self.assertEqual(state.registrations, 1)
                        self.assertEqual(len(state.registered.colors), 18)
                        self.assertIsNone(state.registered.toolbarBackground)
                        self.assertEqual(state.bitmapCalls, 1)

    def test_unsupported_firmware_skips_registration(self):
        for runtime in RUNTIMES:
            for path in THEMES:
                with self.subTest(lua=runtime.__module__, theme=path.parent.name):
                    state = execute(path.read_text(), runtime, supported=False)
                    self.assertEqual(state.registrations, 0)
                    self.assertEqual(state.bitmapCalls, 0)

    def test_downloaded_lua_executes_from_suite_package_root(self):
        checked = set()
        for release in RELEASES_ROOT.glob(f"*-v{THEME_VERSION}.zip"):
            with zipfile.ZipFile(release) as archive:
                manifest = json.loads(archive.read("ethos_lua_manifest.json"))
                source = archive.read("main.lua").decode("utf-8")
                checked.add(manifest["folder"])
                for width in (480, 800):
                    with self.subTest(release=release.name, width=width):
                        state = execute(source, width=width)
                        self.assertEqual(state.registered.name, manifest["name"])
                        self.assertIn(state.registered.toolbarBackground.path, archive.namelist())
        self.assertEqual(checked, {p.parent.name for p in THEMES})


if __name__ == "__main__":
    unittest.main()
