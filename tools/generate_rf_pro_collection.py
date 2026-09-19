from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from palette_quality import polish_lua_source
from theme_lib import (
    add_toolbar_logo,
    ETHOS26_RELEASE_NOTES,
    ETHOS26_SUPPORT,
    INIT_GUARD_LUA,
    RELEASES_ROOT,
    SELECTOR_LUA,
    THEMES_ROOT,
    THEME_VERSION,
    X20_SIZE,
    contrasting,
    downscale_to_x18,
    save_png,
    toolbar_call,
    write_release,
    zip_install_instructions,
)

THEMES = [
    {"slug":"violet","folder":"theme-rf-violet-pro","name":"RF Violet Pro","key":"RFVio","manifest_key":"mbwallace1390-theme-RFVio","accent":(177,76,255),"secondary_bg":(37,28,52),"button_border":(74,54,96),"inactive":(137,119,158),"page_bg":(13,8,20),"primary_bg":(24,16,34)},
    {"slug":"emerald","folder":"theme-rf-emerald-pro","name":"RF Emerald Pro","key":"RFEmer","manifest_key":"mbwallace1390-theme-RFEmer","accent":(0,214,143),"secondary_bg":(22,48,43),"button_border":(44,86,74),"inactive":(104,151,137),"page_bg":(7,17,15),"primary_bg":(13,29,26)},
    {"slug":"ember","folder":"theme-rf-ember-pro","name":"RF Ember Pro","key":"RFEmbr","manifest_key":"mbwallace1390-theme-RFEmbr","accent":(255,106,0),"secondary_bg":(53,32,20),"button_border":(99,60,34),"inactive":(166,127,102),"page_bg":(20,10,5),"primary_bg":(34,18,10)},
    {"slug":"magenta","folder":"theme-rf-magenta-pro","name":"RF Magenta Pro","key":"RFMagn","manifest_key":"mbwallace1390-theme-RFMagn","accent":(255,62,164),"secondary_bg":(54,25,43),"button_border":(103,49,79),"inactive":(172,112,146),"page_bg":(20,7,15),"primary_bg":(34,13,26)},
    {"slug":"cyan","folder":"theme-rf-cyan-pro","name":"RF Cyan Pro","key":"RFCyan","manifest_key":"mbwallace1390-theme-RFCyan","accent":(0,212,255),"secondary_bg":(20,43,52),"button_border":(39,79,94),"inactive":(102,150,163),"page_bg":(5,15,20),"primary_bg":(10,27,34)},
    {"slug":"crimson","folder":"theme-rf-crimson-pro","name":"RF Crimson Pro","key":"RFCrim","manifest_key":"mbwallace1390-theme-RFCrim","accent":(255,51,79),"secondary_bg":(54,25,32),"button_border":(101,47,58),"inactive":(166,109,119),"page_bg":(20,7,10),"primary_bg":(34,13,18)},
    {"slug":"gold","folder":"theme-rf-gold-pro","name":"RF Gold Pro","key":"RFGold","manifest_key":"mbwallace1390-theme-RFGold","accent":(255,196,0),"secondary_bg":(53,45,20),"button_border":(98,82,34),"inactive":(165,149,101),"page_bg":(19,15,4),"primary_bg":(33,27,9)},
    {"slug":"teal","folder":"theme-rf-teal-pro","name":"RF Teal Pro","key":"RFTeal","manifest_key":"mbwallace1390-theme-RFTeal","accent":(0,200,192),"secondary_bg":(19,47,46),"button_border":(38,84,82),"inactive":(101,150,147),"page_bg":(5,17,17),"primary_bg":(9,29,29)},
    {"slug":"lime","folder":"theme-rf-lime-pro","name":"RF Lime Pro","key":"RFLime","manifest_key":"mbwallace1390-theme-RFLime","accent":(168,240,0),"secondary_bg":(42,52,19),"button_border":(76,94,34),"inactive":(142,165,100),"page_bg":(13,19,4),"primary_bg":(23,33,8)},
]


def rgb_lua(color: tuple[int, int, int]) -> str:
    return f"lcd.RGB(0x{color[0]:02X}, 0x{color[1]:02X}, 0x{color[2]:02X})"


def make_toolbar(accent: tuple[int, int, int], page_bg: tuple[int, int, int], primary_bg: tuple[int, int, int]) -> Image.Image:
    width, height = X20_SIZE
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    for y in range(height):
        t = y / (height - 1)
        color = tuple(round(page_bg[i] * (1 - t) + primary_bg[i] * t) for i in range(3))
        draw.line((0, y, width - 1, y), fill=color)

    for offset, strength in [(-3, 0.08), (-2, 0.16), (-1, 0.34), (0, 0.92), (1, 0.28), (2, 0.10)]:
        y = 35 + offset
        base = image.getpixel((0, y))
        color = tuple(round(base[i] * (1 - strength) + accent[i] * strength) for i in range(3))
        draw.line((0, y, width - 1, y), fill=color)

    edge = tuple(max(value - 2, 0) for value in page_bg)
    draw.line((0, height - 1, width - 1, height - 1), fill=edge)
    return image


def build_theme(theme: dict[str, object]) -> None:
    folder = str(theme["folder"])
    name = str(theme["name"])
    key = str(theme["key"])
    slug = str(theme["slug"])
    theme_dir = THEMES_ROOT / folder

    if theme_dir.exists():
        shutil.rmtree(theme_dir)
    theme_dir.mkdir(parents=True)
    RELEASES_ROOT.mkdir(parents=True, exist_ok=True)

    large_name = f"toolbar-{folder.removeprefix('theme-')}.png"
    small_name = f"toolbar-{folder.removeprefix('theme-')}-x18.png"
    large_art = make_toolbar(theme["accent"], theme["page_bg"], theme["primary_bg"])
    save_png(large_art, theme_dir / large_name)
    save_png(downscale_to_x18(large_art), theme_dir / small_name)

    main_lua = f'''-- {name}
-- Lightweight RF Pro outline-focus color variant.
{SELECTOR_LUA}local function init()
{INIT_GUARD_LUA}    system.registerTheme({{
        key = "{key}",
        name = "{name}",
        roundButtons = false,
        focusStyle = "outline",
        colors = {{
            lcd.RGB(0xF4, 0xF7, 0xFB), -- PRIMARY_COLOR
            {rgb_lua(theme["secondary_bg"])}, -- SECONDARY_BGCOLOR
            {rgb_lua(theme["accent"])}, -- HIGHLIGHT_COLOR
            {rgb_lua(contrasting(theme["accent"], (255, 255, 255), theme["primary_bg"]))}, -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x68, 0x74, 0x86), -- DISABLE_COLOR
            {rgb_lua(theme["primary_bg"])}, -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xB7, 0xC5, 0xD8), -- SECONDARY_COLOR
            lcd.RGB(0x42, 0xE6, 0x8A), -- SAFE_COLOR
            {rgb_lua(theme["page_bg"])}, -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x5A, 0x5F), -- ERROR_COLOR
            {rgb_lua(theme["accent"])}, -- ACTIVE_COLOR
            {rgb_lua(theme["inactive"])}, -- INACTIVE_COLOR
            {rgb_lua(theme["accent"])}, -- BUTTON_BORDER_ACTIVE_COLOR
            {rgb_lua(theme["button_border"])}, -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC8, 0x57), -- WARNING_COLOR
            lcd.RGB(0x08, 0x11, 0x0D), -- SAFE_CONTRASTING_COLOR
            {rgb_lua(theme["page_bg"])}, -- TOPLCD_BGCOLOR (XE/S)
        }},
        toolbarBackground = {toolbar_call(large_name, small_name)},
    }})
end

return {{
    init = init
}}
'''
    (theme_dir / "main.lua").write_text(polish_lua_source(main_lua), encoding="utf-8", newline="\n")

    manifest = {
        "manifestVersion": 1,
        "name": name,
        "key": theme["manifest_key"],
        "version": THEME_VERSION,
        "releaseNotes": {
            "format": "markdown",
            "content": (
                f"{ETHOS26_RELEASE_NOTES} "
                f"First stable {name} release using the proven RF Pro outline-focus layout, "
                "square controls, and responsive X18/X20 toolbar. Automatically selects 464x50 "
                "artwork on standard X18 radios and 784x50 artwork on 800px radios."
            ),
        },
        "folder": folder,
        "files": ["main.lua", "toolbar-*"],
    }
    (theme_dir / "ethos_lua_manifest.json").write_text(json.dumps(manifest, indent=4) + "\n", encoding="utf-8", newline="\n")

    readme = f'''# {name} v{THEME_VERSION}

{ETHOS26_SUPPORT}

{zip_install_instructions(folder)}

A lightweight FrSky ETHOS theme based on the proven RF Blue Pro design.

- Bright {slug} outline focus
- Dark square controls
- Clear active, inactive, and disabled states
- Responsive 784x50 X20 / 464x50 X18 toolbar
- ETHOS-safe internal key `{key}`
- Installs beside every other RF Pro theme

To install from repository sources, copy the complete `{folder}` folder into the transmitter's `scripts` folder, restart, and select **{name}** under **System > General > Theme**.

`main.luac` is intentionally omitted so ETHOS creates a fresh compiled copy.
'''
    (theme_dir / "README.md").write_text(readme, encoding="utf-8", newline="\n")

    add_toolbar_logo(theme_dir, folder.removeprefix("theme-"))
    write_release(theme_dir, RELEASES_ROOT / f"RF-{slug.title()}-Pro-v{THEME_VERSION}.zip")


if __name__ == "__main__":
    for theme_definition in THEMES:
        build_theme(theme_definition)
