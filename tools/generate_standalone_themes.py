from __future__ import annotations

import colorsys
import json
import shutil
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw

from png_optimize import optimize_png

ROOT = Path(__file__).resolve().parents[1]
THEMES_ROOT = ROOT / "themes"
RELEASES_ROOT = ROOT / "releases"

# family, slug, display name, short key, focus color, active color, toolbar style
THEMES = [
    ("Retro Instrument","amber-instrument","Amber Instrument","Amber","#FFB000","#FFB000","scanline"),
    ("Retro Instrument","phosphor-green","Phosphor Green","PhosGr","#54FF54","#54FF54","scanline"),
    ("Retro Instrument","ice-instrument","Ice Instrument","IceIns","#8EEBFF","#8EEBFF","instrument"),
    ("Soft","soft-lavender","Soft Lavender","SoftLav","#B79CFF","#B79CFF","soft"),
    ("Soft","soft-mint","Soft Mint","SMint","#91E7C1","#91E7C1","soft"),
    ("Soft","soft-coral","Soft Coral","SCoral","#FF9A8B","#FF9A8B","soft"),
    ("Soft","soft-sky","Soft Sky","SSky","#8FD3FF","#8FD3FF","soft"),
    ("OLED Stealth","oled-blue","OLED Blue","OLBlue","#2F8CFF","#2F8CFF","oled"),
    ("OLED Stealth","oled-red","OLED Red","OLRed","#FF3B4F","#FF3B4F","oled"),
    ("OLED Stealth","oled-green","OLED Green","OLGrn","#3CFF7A","#3CFF7A","oled"),
    ("OLED Stealth","oled-white","OLED White","OLWht","#F5F7FA","#F5F7FA","oled"),
    ("Daylight","daylight-blue","Daylight Blue","DayBlu","#006EDC","#006EDC","daylight"),
    ("Daylight","daylight-orange","Daylight Orange","DayOrg","#E86E00","#E86E00","daylight"),
    ("Daylight","daylight-green","Daylight Green","DayGrn","#138A4B","#138A4B","daylight"),
    ("Industrial","carbon","Carbon","Carbon","#00B7FF","#00B7FF","carbon"),
    ("Industrial","gunmetal","Gunmetal","Gunmet","#7AA7C7","#7AA7C7","brushed"),
    ("Industrial","hazard","Hazard","Hazard","#FFD000","#FFD000","hazard"),
    ("Industrial","titanium","Titanium","Titani","#C8D2DC","#C8D2DC","brushed"),
    ("Two-Tone","violet-circuit","Violet Circuit","VioCkt","#A855F7","#00D4FF","twotone"),
    ("Two-Tone","blue-vector","Blue Vector","BluVec","#208BFF","#43E97B","twotone"),
    ("Two-Tone","ember-signal","Ember Signal","EmbSig","#FF8A00","#FF3B30","twotone"),
    ("Two-Tone","neon-fusion","Neon Fusion","NeoFus","#00D7FF","#FF3EA5","twotone"),
]


def rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def mix(a: tuple[int, int, int], b: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(round(a[i] * (1 - amount) + b[i] * amount) for i in range(3))


def tint_dark(accent: tuple[int, int, int], level: float, saturation: float = 0.38) -> tuple[int, int, int]:
    h, s, _ = colorsys.rgb_to_hsv(*(v / 255 for v in accent))
    r, g, b = colorsys.hsv_to_rgb(h, min(s, saturation), level)
    return round(r * 255), round(g * 255), round(b * 255)


def palette(family: str, focus: tuple[int, int, int], active: tuple[int, int, int], slug: str) -> dict[str, object]:
    white = (245, 247, 250)
    black = (0, 0, 0)
    if family == "Soft":
        page = tint_dark(focus, .14, .28)
        primary_bg = tint_dark(focus, .20, .25)
        secondary_bg = tint_dark(focus, .27, .24)
        return dict(round=True, focus_style="invert", primary=white, secondary_bg=secondary_bg,
                    highlight=focus, highlight_contrast=tint_dark(focus, .16, .35), disabled=mix(primary_bg, white, .38),
                    primary_bg=primary_bg, secondary=mix(focus, white, .50), safe=(140, 231, 180), page=page,
                    error=(255, 117, 128), active=active, inactive=mix(primary_bg, white, .46),
                    active_border=mix(focus, white, .20), border=mix(primary_bg, white, .27), warning=(255, 208, 117),
                    safe_contrast=(20, 42, 30))
    if family == "OLED Stealth":
        page = black
        primary_bg = tint_dark(focus, .045, .32)
        secondary_bg = tint_dark(focus, .085, .30)
        return dict(round=False, focus_style="outline", primary=white, secondary_bg=secondary_bg,
                    highlight=focus, highlight_contrast=black if sum(focus) > 500 else white, disabled=(72, 78, 86),
                    primary_bg=primary_bg, secondary=mix(focus, white, .55), safe=(60, 255, 122), page=page,
                    error=(255, 64, 79), active=active, inactive=mix(primary_bg, white, .38),
                    active_border=active, border=mix(primary_bg, white, .20), warning=(255, 196, 55),
                    safe_contrast=(0, 18, 5))
    if family == "Daylight":
        page = mix(white, focus, .035)
        secondary_bg = mix((232, 235, 238), focus, .08)
        return dict(round=True, focus_style="invert", primary=(18, 24, 30), secondary_bg=secondary_bg,
                    highlight=focus, highlight_contrast=white, disabled=(145, 153, 161), primary_bg=(255, 255, 255),
                    secondary=mix((52, 65, 78), focus, .10), safe=(20, 145, 80), page=page, error=(204, 40, 50),
                    active=active, inactive=(105, 119, 132), active_border=active,
                    border=mix((188, 194, 200), focus, .06), warning=(190, 115, 0), safe_contrast=white)
    if family == "Industrial":
        if slug == "hazard":
            page, primary_bg, secondary_bg = (14, 14, 11), (31, 30, 24), (48, 46, 35)
        elif slug == "titanium":
            page, primary_bg, secondary_bg = (31, 36, 41), (47, 53, 59), (65, 72, 79)
        elif slug == "gunmetal":
            page, primary_bg, secondary_bg = (22, 27, 31), (34, 40, 46), (48, 56, 64)
        else:
            page, primary_bg, secondary_bg = (12, 14, 17), (22, 26, 31), (34, 39, 45)
        return dict(round=False, focus_style="outline", primary=white, secondary_bg=secondary_bg,
                    highlight=focus, highlight_contrast=(18, 22, 26), disabled=mix(primary_bg, white, .35),
                    primary_bg=primary_bg, secondary=mix(focus, white, .54), safe=(63, 235, 127), page=page,
                    error=(255, 68, 77), active=active, inactive=mix(primary_bg, white, .43),
                    active_border=mix(active, white, .10), border=mix(primary_bg, white, .22),
                    warning=focus if slug == "hazard" else (255, 199, 56), safe_contrast=(5, 22, 10))
    page = tint_dark(focus, .065, .52)
    primary_bg = tint_dark(focus, .12, .48)
    secondary_bg = tint_dark(focus, .18, .44)
    primary_text = mix(focus, white, .62) if family == "Retro Instrument" else white
    return dict(round=False, focus_style="outline", primary=primary_text, secondary_bg=secondary_bg,
                highlight=focus, highlight_contrast=tint_dark(focus, .08, .55), disabled=mix(primary_bg, white, .34),
                primary_bg=primary_bg, secondary=mix(focus, white, .52), safe=(78, 239, 132), page=page,
                error=(255, 72, 77), active=active, inactive=mix(primary_bg, white, .40),
                active_border=active, border=mix(primary_bg, white, .23), warning=(255, 199, 68),
                safe_contrast=(7, 24, 12))


def lua_color(c: tuple[int, int, int]) -> str:
    return f"lcd.RGB(0x{c[0]:02X}, 0x{c[1]:02X}, 0x{c[2]:02X})"


def toolbar(path: Path, style: str, page: tuple[int, int, int], primary: tuple[int, int, int], focus: tuple[int, int, int], active: tuple[int, int, int]) -> None:
    w, h = 784, 50
    image = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(image)
    for y in range(h):
        draw.line((0, y, w - 1, y), fill=mix(page, primary, y / (h - 1)))
    if style == "scanline":
        for y in range(2, h, 4):
            draw.line((0, y, w - 1, y), fill=mix(page, focus, .05))
        draw.line((0, 35, w - 1, 35), fill=mix(primary, focus, .78))
        for x in range(20, w, 48):
            draw.line((x, 37, x, 43), fill=mix(primary, focus, .38))
    elif style == "instrument":
        draw.line((0, 34, w - 1, 34), fill=mix(primary, focus, .72))
        for x in range(12, w, 32):
            draw.line((x, 36, x, 43 if (x // 32) % 4 == 0 else 40), fill=mix(primary, focus, .55))
    elif style == "soft":
        for off, strength in [(-4, .06), (-3, .10), (-2, .16), (-1, .25), (0, .42), (1, .20), (2, .10)]:
            y = 35 + off
            draw.line((0, y, w - 1, y), fill=mix(image.getpixel((0, y)), focus, strength))
    elif style == "oled":
        draw.rectangle((0, 0, w - 1, h - 1), fill=page)
        draw.line((0, 36, w - 1, 36), fill=mix(page, focus, .92))
        draw.line((0, 37, w - 1, 37), fill=mix(page, focus, .20))
    elif style == "daylight":
        top = mix(page, (255, 255, 255), .55)
        for y in range(h):
            draw.line((0, y, w - 1, y), fill=mix(top, primary, y / (h - 1) * .30))
        draw.line((0, 36, w - 1, 36), fill=focus)
        draw.line((0, 37, w - 1, 37), fill=mix(primary, focus, .25))
    elif style == "carbon":
        for y in range(0, h, 4):
            for x in range(0, w, 8):
                amount = .045 if ((x // 8) + (y // 4)) % 2 else .015
                draw.rectangle((x, y, x + 7, y + 3), fill=mix(primary, (255, 255, 255), amount))
        draw.line((0, 36, w - 1, 36), fill=focus)
    elif style == "brushed":
        for y in range(h):
            draw.line((0, y, w - 1, y), fill=mix(image.getpixel((0, y)), (255, 255, 255), .035 if y % 3 == 0 else .012))
        draw.line((0, 36, w - 1, 36), fill=mix(primary, focus, .78))
    elif style == "hazard":
        draw.rectangle((0, 34, w - 1, 43), fill=(18, 18, 14))
        for x in range(-20, w + 20, 44):
            draw.polygon([(x, 43), (x + 10, 43), (x + 28, 34), (x + 18, 34)], fill=focus)
    elif style == "twotone":
        draw.line((0, 34, w - 1, 34), fill=mix(primary, focus, .92))
        draw.line((0, 37, w - 1, 37), fill=mix(primary, active, .92))
        for x in range(0, w, 56):
            draw.line((x, 34, x + 24, 34), fill=focus)
            draw.line((x + 28, 37, x + 52, 37), fill=active)
    draw.line((0, h - 1, w - 1, h - 1), fill=mix(page, (0, 0, 0), .35))
    image.save(path, optimize=True)
    optimize_png(path)


def build(defn: tuple[str, str, str, str, str, str, str]) -> None:
    family, slug, name, key, focus_hex, active_hex, style = defn
    focus, active = rgb(focus_hex), rgb(active_hex)
    p = palette(family, focus, active, slug)
    folder = f"theme-{slug}"
    theme_dir = THEMES_ROOT / folder
    if theme_dir.exists():
        shutil.rmtree(theme_dir)
    theme_dir.mkdir(parents=True)
    RELEASES_ROOT.mkdir(parents=True, exist_ok=True)
    toolbar_name = f"toolbar-{slug}.png"
    toolbar(theme_dir / toolbar_name, style, p["page"], p["primary_bg"], focus, active)

    roles = [
        ("PRIMARY_COLOR", p["primary"]), ("SECONDARY_BGCOLOR", p["secondary_bg"]),
        ("HIGHLIGHT_COLOR", p["highlight"]), ("HIGHLIGHT_CONTRASTING_COLOR", p["highlight_contrast"]),
        ("DISABLE_COLOR", p["disabled"]), ("PRIMARY_BGCOLOR", p["primary_bg"]), ("OVERLAY_COLOR", None),
        ("SECONDARY_COLOR", p["secondary"]), ("SAFE_COLOR", p["safe"]), ("PAGE_BGCOLOR", p["page"]),
        ("ERROR_COLOR", p["error"]), ("ACTIVE_COLOR", p["active"]), ("INACTIVE_COLOR", p["inactive"]),
        ("BUTTON_BORDER_ACTIVE_COLOR", p["active_border"]), ("BUTTON_BORDER_COLOR", p["border"]),
        ("WARNING_COLOR", p["warning"]), ("SAFE_CONTRASTING_COLOR", p["safe_contrast"]),
        ("TOPLCD_BGCOLOR", p["page"]),
    ]
    color_lines = [f"            {'COLOR_BLACK' if value is None else lua_color(value)}, -- {role}" for role, value in roles]
    lua = f'''-- {name}
-- Lightweight standalone ETHOS theme.
local function init()
    system.registerTheme({{
        key = "{key}",
        name = "{name}",
        roundButtons = {str(p["round"]).lower()},
        focusStyle = "{p["focus_style"]}",
        colors = {{
{chr(10).join(color_lines)}
        }},
        toolbarBackground = lcd.loadBitmap("{toolbar_name}"),
    }})
end

return {{ init = init }}
'''
    (theme_dir / "main.lua").write_text(lua, encoding="utf-8", newline="\n")
    manifest = {
        "manifestVersion": 1,
        "name": name,
        "key": f"mbwallace1390-theme-{key}",
        "version": "1.0.0",
        "releaseNotes": {"format": "markdown", "content": f"First stable {name} release from the {family} family."},
        "folder": folder,
        "files": ["main.lua", "toolbar-*"],
    }
    (theme_dir / "ethos_lua_manifest.json").write_text(json.dumps(manifest, indent=4) + "\n", encoding="utf-8", newline="\n")
    (theme_dir / "README.md").write_text(
        f"# {name} v1.0.0\n\n**Family:** {family}\n\nA lightweight standalone FrSky ETHOS theme.\n\n"
        f"- Focus: `{p['focus_style']}`\n- Controls: {'rounded' if p['round'] else 'square'}\n- Internal key: `{key}`\n"
        f"- Static 784x50 toolbar\n\nCopy `{folder}` into the transmitter `scripts` folder, restart, and select **{name}**.\n",
        encoding="utf-8",
        newline="\n",
    )
    release = RELEASES_ROOT / f"{'-'.join(word.capitalize() for word in slug.split('-'))}-v1.0.0.zip"
    if release.exists():
        release.unlink()
    with zipfile.ZipFile(release, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        info = zipfile.ZipInfo(folder + "/")
        info.external_attr = (0o40777 << 16) | 0x10
        archive.writestr(info, b"")
        for item in sorted(theme_dir.iterdir(), key=lambda x: x.name):
            archive.write(item, f"{folder}/{item.name}")


if __name__ == "__main__":
    keys = [item[3] for item in THEMES]
    if len(keys) != len(set(keys)) or any(len(key) > 7 for key in keys):
        raise SystemExit("Theme keys must be unique and <=7 characters")
    for theme in THEMES:
        build(theme)
