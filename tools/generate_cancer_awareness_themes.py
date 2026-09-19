from __future__ import annotations

import json
import math
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from png_optimize import optimize_png
from palette_quality import polish_lua_source
from theme_lib import (
    add_toolbar_logo,
    ETHOS26_RELEASE_NOTES,
    ETHOS26_SUPPORT,
    INIT_GUARD_LUA,
    PREVIEWS_ROOT,
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

# slug, display name, ETHOS key, awareness label, ribbon color, active color,
# page background, primary background, secondary background, border, artwork style
THEMES = [
    ("pink-hope", "Pink Hope", "PinkHp", "Breast Cancer Awareness", "#F48FB1", "#FFD1E1", "#1A0E15", "#321824", "#4A2535", "#7B4058", "hearts"),
    ("golden-courage", "Golden Courage", "GoldCr", "Childhood Cancer Awareness", "#F4C542", "#FFF0A6", "#17130A", "#302812", "#4A3E1B", "#756126", "stars"),
    ("lavender-unity", "Lavender Unity", "LavUnt", "All Cancers Awareness", "#B79CFF", "#E2D7FF", "#14101D", "#29203B", "#3C3055", "#665285", "unity"),
    ("teal-strength", "Teal Strength", "TealStr", "Ovarian Cancer Awareness", "#22C7B8", "#8EF3E9", "#071817", "#10302D", "#194943", "#2C746B", "waves"),
    ("blue-resolve", "Blue Resolve", "BluRsv", "Prostate Cancer Awareness", "#7EC8FF", "#D3EEFF", "#09131C", "#13293B", "#1D3E56", "#356685", "shield"),
    ("orange-warrior", "Orange Warrior", "OrgWar", "Leukemia Awareness", "#FF8A2A", "#FFD2A8", "#1A0E05", "#351C0A", "#512B10", "#84491C", "flame"),
    ("purple-hope", "Purple Hope", "PurHope", "Pancreatic Cancer Awareness", "#8D5AD8", "#D7B8FF", "#110B19", "#251735", "#38234F", "#604080", "rays"),
    ("pearl-breath", "Pearl Breath", "PearlBr", "Lung Cancer Awareness", "#E7ECEF", "#FFFFFF", "#11161A", "#242D33", "#36434B", "#667580", "breath"),
    ("royal-blue-strong", "Royal Blue Strong", "RoyBlue", "Colorectal Cancer Awareness", "#275DCE", "#A9C8FF", "#080E1A", "#111F38", "#1A3156", "#31548A", "geometry"),
    ("green-courage", "Green Courage", "GrnCour", "Liver Cancer Awareness", "#36B96B", "#A8F0C0", "#07150C", "#102B19", "#194126", "#2D7044", "leaves"),
]


def rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def mix(a: tuple[int, int, int], b: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(round(a[i] * (1 - amount) + b[i] * amount) for i in range(3))


def lua_rgb(value: tuple[int, int, int]) -> str:
    return f"lcd.RGB(0x{value[0]:02X}, 0x{value[1]:02X}, 0x{value[2]:02X})"


def ribbon_points(cx: int, top: int, scale: float = 1.0):
    """Return polygons that form a generic folded awareness ribbon."""
    s = scale
    left_loop = [
        (cx, top),
        (cx - int(9*s), top + int(5*s)),
        (cx - int(14*s), top + int(15*s)),
        (cx - int(8*s), top + int(22*s)),
        (cx, top + int(14*s)),
        (cx + int(5*s), top + int(7*s)),
    ]
    right_loop = [
        (cx, top),
        (cx + int(9*s), top + int(5*s)),
        (cx + int(14*s), top + int(15*s)),
        (cx + int(8*s), top + int(22*s)),
        (cx, top + int(14*s)),
        (cx - int(5*s), top + int(7*s)),
    ]
    left_tail = [
        (cx - int(2*s), top + int(13*s)),
        (cx - int(11*s), top + int(31*s)),
        (cx - int(2*s), top + int(28*s)),
        (cx + int(5*s), top + int(16*s)),
    ]
    right_tail = [
        (cx + int(2*s), top + int(13*s)),
        (cx + int(11*s), top + int(31*s)),
        (cx + int(2*s), top + int(28*s)),
        (cx - int(5*s), top + int(16*s)),
    ]
    return left_loop, right_loop, left_tail, right_tail


def draw_ribbon(draw: ImageDraw.ImageDraw, cx: int, top: int, ribbon: tuple[int, int, int], scale: float = 1.0) -> None:
    left_loop, right_loop, left_tail, right_tail = ribbon_points(cx, top, scale)
    dark = mix(ribbon, (0, 0, 0), 0.30)
    light = mix(ribbon, (255, 255, 255), 0.23)
    draw.polygon(left_tail, fill=dark)
    draw.polygon(right_tail, fill=ribbon)
    draw.polygon(left_loop, fill=light)
    draw.polygon(right_loop, fill=ribbon)
    draw.line(left_loop + [left_loop[0]], fill=light, width=max(1, round(scale)))
    draw.line(right_loop + [right_loop[0]], fill=dark, width=max(1, round(scale)))


def draw_toolbar(theme) -> Image.Image:
    slug, _, _, _, ribbon_hex, active_hex, page_hex, primary_hex, _, _, style = theme
    width, height = X20_SIZE
    ribbon, active, page, primary = map(rgb, (ribbon_hex, active_hex, page_hex, primary_hex))
    image = Image.new("RGB", (width, height), page)
    draw = ImageDraw.Draw(image)

    for y in range(height):
        draw.line((0, y, width - 1, y), fill=mix(page, primary, y / (height - 1)))

    # Repeating fine accent line keeps the toolbar readable across the full width.
    draw.line((0, 39, width - 1, 39), fill=mix(page, ribbon, 0.82), width=2)
    draw_ribbon(draw, 32, 7, ribbon, 1.05)

    if style == "hearts":
        for x in range(92, width, 92):
            draw.arc((x, 12, x + 12, 24), 190, 355, fill=mix(page, ribbon, .58), width=2)
            draw.arc((x + 10, 12, x + 22, 24), 185, 350, fill=mix(page, ribbon, .58), width=2)
            draw.line((x + 1, 19, x + 11, 30), fill=mix(page, ribbon, .58), width=2)
            draw.line((x + 21, 19, x + 11, 30), fill=mix(page, ribbon, .58), width=2)
    elif style == "stars":
        for x in range(88, width, 68):
            y = 17 if (x // 68) % 2 else 25
            draw.ellipse((x, y, x + 3, y + 3), fill=active)
            draw.line((x - 3, y + 1, x + 6, y + 1), fill=mix(page, ribbon, .56))
            draw.line((x + 1, y - 3, x + 1, y + 6), fill=mix(page, ribbon, .56))
    elif style == "unity":
        for x in range(90, width, 74):
            draw.arc((x, 10, x + 26, 36), 30, 330, fill=mix(page, ribbon, .62), width=2)
            draw.arc((x + 11, 10, x + 37, 36), 210, 150, fill=mix(page, active, .62), width=2)
    elif style == "waves":
        points = []
        for x in range(78, width):
            y = 23 + round(5 * math.sin((x - 78) / 24))
            points.append((x, y))
        draw.line(points, fill=mix(page, ribbon, .68), width=2)
        draw.line([(x, y + 7) for x, y in points], fill=mix(page, active, .35), width=1)
    elif style == "shield":
        for x in range(94, width, 95):
            draw.polygon([(x, 9), (x + 23, 14), (x + 20, 30), (x + 11, 36), (x + 2, 30), (x - 1, 14)], outline=mix(page, ribbon, .65))
            draw.line((x + 11, 15, x + 11, 31), fill=mix(page, active, .55))
    elif style == "flame":
        for x in range(94, width, 88):
            draw.polygon([(x + 10, 34), (x + 2, 25), (x + 8, 12), (x + 14, 23), (x + 20, 8), (x + 25, 24), (x + 19, 34)], outline=mix(page, ribbon, .66))
    elif style == "rays":
        for x in range(102, width, 104):
            for offset in (-13, 0, 13):
                draw.line((x, 22, x + 26, 22 + offset), fill=mix(page, ribbon if offset else active, .55), width=2)
    elif style == "breath":
        for row in range(3):
            y = 13 + row * 9
            for x in range(86 + row * 18, width, 130):
                draw.arc((x, y - 4, x + 80, y + 8), 190, 345, fill=mix(page, ribbon, .54), width=2)
    elif style == "geometry":
        for x in range(86, width, 64):
            draw.line((x, 11, x + 28, 25), fill=mix(page, ribbon, .65), width=2)
            draw.line((x + 28, 25, x, 36), fill=mix(page, active, .47), width=2)
    elif style == "leaves":
        for x in range(90, width, 82):
            draw.arc((x, 12, x + 24, 34), 80, 270, fill=mix(page, ribbon, .68), width=2)
            draw.arc((x + 14, 11, x + 38, 33), 270, 100, fill=mix(page, active, .48), width=2)
            draw.line((x + 18, 16, x + 18, 35), fill=mix(page, ribbon, .52))

    draw.line((0, height - 1, width - 1, height - 1), fill=mix(page, (0, 0, 0), .38))
    return image


def palette(theme):
    _, _, _, _, ribbon_hex, active_hex, page_hex, primary_hex, secondary_hex, border_hex, _ = theme
    ribbon, active, page, primary, secondary, border = map(rgb, (ribbon_hex, active_hex, page_hex, primary_hex, secondary_hex, border_hex))
    primary_text = (245, 247, 250)
    highlight_contrast = (12, 10, 13) if sum(ribbon) > 430 else contrasting(ribbon, (255, 255, 255), primary)
    return {
        "PRIMARY_COLOR": primary_text,
        "SECONDARY_BGCOLOR": secondary,
        "HIGHLIGHT_COLOR": ribbon,
        "HIGHLIGHT_CONTRASTING_COLOR": highlight_contrast,
        "DISABLE_COLOR": mix(primary, primary_text, .38),
        "PRIMARY_BGCOLOR": primary,
        "SECONDARY_COLOR": mix(ribbon, primary_text, .55),
        "SAFE_COLOR": (86, 226, 137),
        "PAGE_BGCOLOR": page,
        "ERROR_COLOR": (255, 78, 88),
        "ACTIVE_COLOR": active,
        "INACTIVE_COLOR": mix(primary, primary_text, .44),
        "BUTTON_BORDER_ACTIVE_COLOR": active,
        "BUTTON_BORDER_COLOR": border,
        "WARNING_COLOR": (255, 199, 72),
        "SAFE_CONTRASTING_COLOR": (7, 24, 12),
        "TOPLCD_BGCOLOR": page,
    }


def build_theme(theme) -> None:
    slug, name, key, awareness, *_ = theme
    folder = f"theme-{slug}"
    theme_dir = THEMES_ROOT / folder
    if theme_dir.exists():
        shutil.rmtree(theme_dir)
    theme_dir.mkdir(parents=True)
    RELEASES_ROOT.mkdir(parents=True, exist_ok=True)

    large_name = f"toolbar-{slug}.png"
    small_name = f"toolbar-{slug}-x18.png"
    large_art = draw_toolbar(theme)
    save_png(large_art, theme_dir / large_name)
    save_png(downscale_to_x18(large_art), theme_dir / small_name)
    colors = palette(theme)
    color_lines = []
    order = [
        "PRIMARY_COLOR", "SECONDARY_BGCOLOR", "HIGHLIGHT_COLOR", "HIGHLIGHT_CONTRASTING_COLOR",
        "DISABLE_COLOR", "PRIMARY_BGCOLOR", "OVERLAY_COLOR", "SECONDARY_COLOR", "SAFE_COLOR",
        "PAGE_BGCOLOR", "ERROR_COLOR", "ACTIVE_COLOR", "INACTIVE_COLOR",
        "BUTTON_BORDER_ACTIVE_COLOR", "BUTTON_BORDER_COLOR", "WARNING_COLOR",
        "SAFE_CONTRASTING_COLOR", "TOPLCD_BGCOLOR",
    ]
    for role in order:
        value = "COLOR_BLACK" if role == "OVERLAY_COLOR" else lua_rgb(colors[role])
        color_lines.append(f"            {value}, -- {role}")

    lua = f'''-- {name}
-- Standalone ETHOS cancer-awareness radio theme.
-- Rotorflight and RF Suite files are not modified.
{SELECTOR_LUA}local function init()
{INIT_GUARD_LUA}    system.registerTheme({{
        key = "{key}",
        name = "{name}",
        roundButtons = false,
        focusStyle = "outline",
        colors = {{
{chr(10).join(color_lines)}
        }},
        toolbarBackground = {toolbar_call(large_name, small_name)},
    }})
end

return {{ init = init }}
'''
    (theme_dir / "main.lua").write_text(polish_lua_source(lua), encoding="utf-8", newline="\n")

    manifest = {
        "manifestVersion": 1,
        "name": name,
        "key": f"mbwallace1390-theme-{key}",
        "version": THEME_VERSION,
        "releaseNotes": {
            "format": "markdown",
            "content": (
                f"{ETHOS26_RELEASE_NOTES} "
                f"First stable {name} release for {awareness}. Includes original generic "
                "awareness-ribbon toolbar artwork and changes only the ETHOS radio theme. "
                "Automatically selects 464x50 artwork on standard X18 radios and 784x50 "
                "artwork on 800px radios."
            ),
        },
        "folder": folder,
        "files": ["main.lua", "toolbar-*"],
    }
    (theme_dir / "ethos_lua_manifest.json").write_text(json.dumps(manifest, indent=4) + "\n", encoding="utf-8", newline="\n")

    readme = f"""# {name} v{THEME_VERSION}

{ETHOS26_SUPPORT}

{zip_install_instructions(folder)}

**Collection:** Cancer Awareness  
**Theme:** {awareness}

A standalone FrSky ETHOS radio theme with original generic awareness-ribbon toolbar artwork.

- Outline focus with square controls
- Unique internal key: `{key}`
- Responsive 784x50 X20 / 464x50 X18 toolbar
- Separate installable package
- Does not modify Rotorflight or RF Suite Lua files

To install from repository sources, copy `{folder}` into the transmitter's `scripts` folder, restart, and select **{name}** under **System > General > Theme**.
"""
    (theme_dir / "README.md").write_text(readme, encoding="utf-8", newline="\n")

    release_name = "-".join(word.capitalize() for word in slug.split("-")) + f"-v{THEME_VERSION}.zip"
    add_toolbar_logo(theme_dir, slug)
    write_release(theme_dir, RELEASES_ROOT / release_name)


def generate_preview():
    from preview_lib import render_collection
    render_collection("cancer-awareness", "Cancer Awareness", [t[0] for t in THEMES])


def main() -> None:
    keys = [theme[2] for theme in THEMES]
    slugs = [theme[0] for theme in THEMES]
    names = [theme[1] for theme in THEMES]
    if len(keys) != len(set(keys)) or any(len(key) > 7 for key in keys):
        raise SystemExit("Theme keys must be unique and no longer than seven characters")
    if len(slugs) != len(set(slugs)) or len(names) != len(set(names)):
        raise SystemExit("Theme names and slugs must be unique")

    for theme in THEMES:
        build_theme(theme)
    generate_preview()
    print(f"Generated {len(THEMES)} separate cancer-awareness themes and one collection preview")


if __name__ == "__main__":
    main()
