"""Execute the catalog in Lua with the documented ETHOS 26.1.2 API surface.

These are API-stub checks, not firmware simulator or radio acceptance tests.
Requires development-only Pillow and lupa; no dependency is shipped to radios.
"""

from __future__ import annotations

import json
from fnmatch import fnmatchcase
import re
import unittest
import zipfile

from lupa.lua52 import LuaRuntime as Lua52
from lupa.lua54 import LuaRuntime as Lua54
from PIL import Image

from theme_lib import RELEASES_ROOT, THEMES_ROOT
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
HEADER_TEXT_THEMES = {"theme-america250", "theme-ink-halo"}

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
        if path == "logo-transparent.png" then
            if bitmapMode == "logo-error" then error("Logo initialization failed") end
            if bitmapMode == "logo-nil" then return nil end
        end
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
        self.assertEqual(len(THEMES), 68)
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
                        has_header_text = path.parent.name in HEADER_TEXT_THEMES
                        expected = allowed | ({"toolbarLogo"} if has_header_text else set())
                        self.assertEqual(set(theme.keys()), expected)
                        self.assertEqual(theme.name, manifest["name"])
                        self.assertTrue(1 <= len(theme.key) <= 7)
                        self.assertIsInstance(theme.roundButtons, bool)
                        self.assertIn(theme.focusStyle, ("invert", "outline", "color"))
                        self.assertEqual(set(theme.colors.keys()), set(range(1, 19)))
                        self.assertTrue(all(isinstance(c, (int, float)) for c in theme.colors.values()))
                        self.assertEqual(state.bitmapCalls, 2 if has_header_text else 1)
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
                        self.assertEqual(state.bitmapCalls, 2 if path.parent.name in HEADER_TEXT_THEMES else 1)

    def test_header_text_has_a_fully_transparent_logo_override(self):
        for folder in sorted(HEADER_TEXT_THEMES):
            path = THEMES_ROOT / folder / "main.lua"
            manifest = json.loads(path.with_name("ethos_lua_manifest.json").read_text())
            for runtime in RUNTIMES:
                for width in (480, 800):
                    with self.subTest(theme=folder, lua=runtime.__module__, width=width):
                        state = execute(path.read_text(), runtime, width)
                        self.assertIsNotNone(state.registered.toolbarLogo,
                                             "A missing override leaves ETHOS over the header inscription")
                        logo = state.registered.toolbarLogo.path
                        self.assertTrue(any(fnmatchcase(logo, pattern) for pattern in manifest["files"]))
                        with Image.open(path.with_name(logo)) as image:
                            self.assertEqual(image.size, (1, 1))
                            self.assertEqual(image.convert("RGBA").getchannel("A").getextrema(), (0, 0))

    def test_logo_load_failure_preserves_background_and_palette(self):
        for folder in sorted(HEADER_TEXT_THEMES):
            path = THEMES_ROOT / folder / "main.lua"
            for runtime in RUNTIMES:
                for width in (480, 800):
                    for mode in ("logo-error", "logo-nil"):
                        with self.subTest(theme=folder, lua=runtime.__module__, width=width, mode=mode):
                            state = execute(path.read_text(), runtime, width, bitmap_mode=mode)
                            self.assertEqual(state.registrations, 1)
                            self.assertEqual(len(state.registered.colors), 18)
                            self.assertIsNotNone(state.registered.toolbarBackground)
                            self.assertIsNone(state.registered.toolbarLogo)
                            self.assertEqual(state.bitmapCalls, 2)

    def test_unsupported_firmware_skips_registration(self):
        for runtime in RUNTIMES:
            for path in THEMES:
                with self.subTest(lua=runtime.__module__, theme=path.parent.name):
                    state = execute(path.read_text(), runtime, supported=False)
                    self.assertEqual(state.registrations, 0)
                    self.assertEqual(state.bitmapCalls, 0)

    def test_downloaded_lua_executes_from_suite_package_root(self):
        checked = set()
        for release in RELEASES_ROOT.glob("*-v*.zip"):
            with zipfile.ZipFile(release) as archive:
                if "ethos_lua_manifest.json" not in archive.namelist():
                    continue
                manifest = json.loads(archive.read("ethos_lua_manifest.json"))
                current = json.loads((THEMES_ROOT / manifest["folder"] / "ethos_lua_manifest.json").read_text())
                if manifest["version"] != current["version"]:
                    continue
                source = archive.read("main.lua").decode("utf-8")
                checked.add(manifest["folder"])
                for width in (480, 800):
                    with self.subTest(release=release.name, width=width):
                        state = execute(source, width=width)
                        self.assertEqual(state.registered.name, manifest["name"])
                        self.assertIn(state.registered.toolbarBackground.path, archive.namelist())
                        if manifest["folder"] in HEADER_TEXT_THEMES:
                            self.assertIsNotNone(state.registered.toolbarLogo)
                            self.assertIn(state.registered.toolbarLogo.path, archive.namelist())
        self.assertEqual(checked, {p.parent.name for p in THEMES})


if __name__ == "__main__":
    unittest.main()
