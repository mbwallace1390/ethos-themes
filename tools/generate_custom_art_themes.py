from __future__ import annotations

import json
import math
import random
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
    X18_SIZE,
    X20_SIZE,
    compose_toolbar_sides,
    save_png,
    toolbar_call,
    write_release,
    zip_install_instructions,
)

# collection, slug, display name, short ETHOS key, release ZIP, artwork style,
# round buttons, focus style, then 16 palette colors:
# primary, secondary bg, highlight, highlight contrast, disabled, primary bg,
# secondary text, safe, page bg, error, active, inactive, active border,
# normal border, warning, safe contrast.
THEMES = [
    ("Flight Systems", "aviation-hud", "Aviation HUD", "AvHUD", f"Aviation-HUD-v{THEME_VERSION}.zip", "hud", False, "outline",
     ["D9FFE2","12271A","62FF86","06140A","55725C","0B1B11","9AEFAC","62FF86","050D08","FF4B4B","B8FF4A","688A70","B8FF4A","294E33","FFD24A","031006"]),
    ("Flight Systems", "midnight-blueprint", "Midnight Blueprint", "MidBpt", f"Midnight-Blueprint-v{THEME_VERSION}.zip", "blueprint", False, "outline",
     ["E7F6FF","143651","62C8FF","071826","6A879B","0D263B","B5E1F8","58E69A","071725","FF5B68","F4F7FA","7898AD","F4F7FA","345C77","FFD06A","071A10"]),
    ("Flight Systems", "rotor-command", "Rotor Command", "RotorCm", f"Rotor-Command-v{THEME_VERSION}.zip", "rotor", False, "outline",
     ["EAF7F7","173638","37D4C9","061A1A","668889","0D2426","A9DEDC","65E68D","061516","FF5058","FF664D","719798","FF664D","315C5E","FFD166","071A0C"]),
    ("Tactical", "woodland-tactical", "Woodland Tactical", "WoodTac", f"Woodland-Tactical-v{THEME_VERSION}.zip", "woodland", False, "outline",
     ["EEF0D8","39432A","B7C96B","171C0C","7B8265","272F1D","CBD2A4","7FE07B","161C11","FF5B4F","E9A441","8D956E","E9A441","586342","F5C65D","0A1808"]),
    ("Tactical", "arctic-tactical", "Arctic Tactical", "ArcTac", f"Arctic-Tactical-v{THEME_VERSION}.zip", "arctic", False, "outline",
     ["17242E","CAD6DC","1679A8","F6FBFE","7B8C96","E6EDF0","3E5D70","168A59","F5F8FA","C93645","0C5D86","8095A1","0C5D86","AABBC4","A76400","FFFFFF"]),
    ("Tactical", "desert-tactical", "Desert Tactical", "DesTac", f"Desert-Tactical-v{THEME_VERSION}.zip", "desert", False, "outline",
     ["2E2418","C9B38C","A85C24","FFF8EA","8C7C64","E3D2B1","624A32","3B8458","F1E7D2","B83832","7B3E17","967E5F","7B3E17","B29B74","A15E00","FFFFFF"]),
    ("Cosmic", "deep-space", "Deep Space", "DSpace", f"Deep-Space-v{THEME_VERSION}.zip", "space", False, "outline",
     ["F4F0FF","241B3D","9C6CFF","130B25","75698F","171126","CDBCF2","54E59A","08060F","FF5370","4EC9FF","81749A","4EC9FF","473763","FFD166","071A10"]),
    ("Cosmic", "lunar-command", "Lunar Command", "Lunar", f"Lunar-Command-v{THEME_VERSION}.zip", "lunar", False, "outline",
     ["F0F2F4","41474E","C8D0D8","1D2227","858C93","2B3036","D2D7DC","74D895","181B1F","FF5A62","E7B04A","929AA2","E7B04A","606972","E7B04A","0B180F"]),
    ("Cosmic", "neon-horizon", "Neon Horizon", "NeoHor", f"Neon-Horizon-v{THEME_VERSION}.zip", "horizon", True, "invert",
     ["F7F1FF","2B1B49","FF4FB8","250A20","806A92","1A1230","D9BAF4","5FE8A5","0B0716","FF4D6D","34D8FF","8B73A0","34D8FF","58366F","FFD166","071A11"]),
    ("Tech & Racing", "circuit-trace", "Circuit Trace", "CirTrce", f"Circuit-Trace-v{THEME_VERSION}.zip", "circuit", False, "outline",
     ["E7F9E8","173B2A","44E57A","06180C","5F806A","0D281B","A9DFB7","44E57A","06150E","FF5360","F0D84D","6D9278","F0D84D","2C5A3E","F0D84D","06180C"]),
    ("Tech & Racing", "racing-division", "Racing Division", "RaceDiv", f"Racing-Division-v{THEME_VERSION}.zip", "racing", False, "invert",
     ["F5F5F5","292929","E73333","FFFFFF","777777","191919","D7D7D7","58D889","0B0B0B","FF3B3B","FFFFFF","8A8A8A","FFFFFF","4A4A4A","FFC54A","07180D"]),
    ("Tech & Racing", "hex-core", "Hex Core", "HexCore", f"Hex-Core-v{THEME_VERSION}.zip", "hex", False, "outline",
     ["F3F7FA","26313D","FF8A3D","231006","72808C","18222C","C0CDD7","54DF91","0B1117","FF4F5E","44C7FF","82919D","44C7FF","3C4E5D","FFC14A","07190E"]),
]

COLLECTIONS = {
    "flight-systems": ("Flight Systems", ["aviation-hud", "midnight-blueprint", "rotor-command"]),
    "tactical": ("Tactical", ["woodland-tactical", "arctic-tactical", "desert-tactical"]),
    "cosmic": ("Cosmic", ["deep-space", "lunar-command", "neon-horizon"]),
    "tech-racing": ("Tech & Racing", ["circuit-trace", "racing-division", "hex-core"]),
}

ROLES = [
    "PRIMARY_COLOR", "SECONDARY_BGCOLOR", "HIGHLIGHT_COLOR",
    "HIGHLIGHT_CONTRASTING_COLOR", "DISABLE_COLOR", "PRIMARY_BGCOLOR",
    "SECONDARY_COLOR", "SAFE_COLOR", "PAGE_BGCOLOR", "ERROR_COLOR",
    "ACTIVE_COLOR", "INACTIVE_COLOR", "BUTTON_BORDER_ACTIVE_COLOR",
    "BUTTON_BORDER_COLOR", "WARNING_COLOR", "SAFE_CONTRASTING_COLOR",
]


def color(value: str) -> tuple[int, int, int]:
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def mix(a, b, amount: float):
    return tuple(round(a[i] * (1 - amount) + b[i] * amount) for i in range(3))


def lua_rgb(value: str) -> str:
    r, g, b = color(value)
    return f"lcd.RGB(0x{r:02X}, 0x{g:02X}, 0x{b:02X})"


def gradient(draw, width, height, top, bottom):
    for y in range(height):
        draw.line((0, y, width - 1, y), fill=mix(top, bottom, y / (height - 1)))


def camo(draw, width, height, colors, seed):
    rng = random.Random(seed)
    draw.rectangle((0, 0, width - 1, height - 1), fill=colors[0])
    for fill in colors[1:]:
        for _ in range(34):
            x, y = rng.randint(-35, width - 5), rng.randint(-10, height - 2)
            w, h = rng.randint(25, 85), rng.randint(7, 23)
            draw.polygon([(x, y+h//2),(x+w//3,y),(x+w,y+h//3),(x+2*w//3,y+h),(x+w//8,y+3*h//4)], fill=fill)


def artwork(draw, style, width, height, page, panel, accent, active, side=0):
    gradient(draw, width, height, page, panel)
    center = width // 2

    if style == "hud":
        draw.line((0, 36, width-1, 36), fill=mix(page, accent, .8))
        for x in range(14, width, 28):
            draw.line((x, 37, x, 45 if x % 112 == 14 else 41), fill=mix(page, accent, .72))
        if side == 0:
            draw.ellipse((center-12, 10, center+12, 34), outline=accent)
            draw.line((center-22,22,center-5,22), fill=accent)
            draw.line((center+5,22,center+22,22), fill=accent)
            draw.line((center,4,center,16), fill=active)
        else:
            for y, half_width in ((10, 15), (18, 24), (26, 15)):
                draw.line((center-half_width,y,center+half_width,y), fill=accent)
    elif style == "blueprint":
        for x in range(0, width, 16):
            draw.line((x,0,x,height-1), fill=mix(page, accent, .28 if x % 64 == 0 else .13))
        for y in range(0, height, 10):
            draw.line((0,y,width-1,y), fill=mix(page, accent, .26 if y % 20 == 0 else .12))
        if side == 0:
            half_width = min(51, center - 16)
            draw.rectangle((center-half_width,8,center+half_width,34), outline=mix(page,accent,.8))
        else:
            draw.arc((center-40,3,center+40,45),190,350,fill=active)
    elif style == "rotor":
        draw.line((0,36,width-1,36), fill=mix(page,accent,.7))
        if side == 0:
            rotor_half_width = min(66, center - 12)
            draw.line((center-rotor_half_width,17,center+rotor_half_width,17), fill=accent, width=2)
            draw.ellipse((center-4,13,center+4,21), fill=active)
            draw.line((center,21,center,32), fill=accent, width=2)
            draw.polygon([(center-20,31),(center+23,31),(center+11,21),(center-10,21)], outline=accent)
            draw.line((center+22,27,center+47,22), fill=accent, width=2)
        else:
            for x in range(16, width - 12, 24):
                draw.line((x,29,x,35), fill=mix(page,accent,.7))
    elif style == "woodland":
        camo(draw,width,height,[color("1A2214"),color("344126"),color("55603A"),color("24291C")],101)
        draw.line((0,39,width-1,39), fill=accent, width=2)
    elif style == "arctic":
        camo(draw,width,height,[color("E8EEF1"),color("BECBD2"),color("93A7B3"),color("D7E2E7")],202)
        draw.line((0,39,width-1,39), fill=accent, width=2)
    elif style == "desert":
        camo(draw,width,height,[color("E5D2AD"),color("C3A777"),color("9E7A4B"),color("D8BE91")],303)
        draw.line((0,39,width-1,39), fill=accent, width=2)
    elif style == "space":
        rng = random.Random(143 + side)
        for _ in range(max(18, width // 6)):
            x, y = rng.randrange(width), rng.randrange(height)
            bright = rng.choice((.3,.45,.65,.9))
            radius = 2 if bright > .8 else 1
            draw.ellipse((x,y,x+radius,y+radius), fill=mix(page,(255,255,255),bright))
        radius = 19 if side == 0 else 22
        planet = accent if side == 0 else active
        draw.ellipse((center-radius,24-radius,center+radius,24+radius),
                     fill=mix(page,planet,.08), outline=mix(page,planet,.4))
    elif style == "lunar":
        surface = mix(panel, accent, .12)
        draw.rectangle((0,27,width-1,height-1), fill=surface)
        rng = random.Random(2049 + side)
        for _ in range(max(10, width // 15)):
            x, y, radius = rng.randrange(width), rng.randrange(27,height), rng.randint(2,8)
            draw.ellipse((x-radius,y-radius//2,x+radius,y+radius//2), outline=mix(surface,page,.35))
        if side == 0:
            draw.arc((center-21,2,center+21,44),0,180,fill=accent,width=2)
        draw.line((0,26,width-1,26), fill=active)
    elif style == "horizon":
        horizon = 29
        draw.line((0,horizon,width-1,horizon), fill=active, width=2)
        if side == 0:
            draw.ellipse((center-28,4,center+28,48), fill=mix(page,accent,.25), outline=accent, width=2)
            for y in range(8,29,5): draw.line((center-25,y,center+25,y), fill=mix(page,accent,.45))
        for x in range(0,width,52): draw.line((center,horizon,x,height-1), fill=mix(page,active,.38))
        for y in (34,39,44,48): draw.line((0,y,width-1,y), fill=mix(page,active,.35))
    elif style == "circuit":
        rng = random.Random(880)
        for row in range(4):
            y, x = 8 + row*11, -10
            while x < width:
                length, jog = rng.randint(18,54), rng.choice((-5,0,5))
                draw.line((x,y,x+length,y), fill=mix(page,accent,.72))
                draw.line((x+length,y,x+length+6,y+jog), fill=mix(page,accent,.72))
                if rng.random() > .55: draw.ellipse((x+length-2,y-2,x+length+2,y+2), fill=active)
                x += length + 12
    elif style == "racing":
        square, y0 = 10, 30
        for y in range(y0,height,square):
            for x in range(0,width,square):
                draw.rectangle((x,y,x+square-1,y+square-1), fill=active if ((x//square)+(y-y0)//square)%2==0 else page)
        for offset in (0,16,32):
            x = center - 16 + offset
            draw.polygon([(x,0),(x+14,0),(x-22,30),(x-36,30)], fill=accent)
        draw.line((0,28,width-1,28), fill=accent, width=2)
    elif style == "hex":
        radius = 10
        vstep = int(math.sqrt(3)*radius)
        for row, y in enumerate(range(-5,height+vstep,vstep)):
            offset = 0 if row % 2 == 0 else int(1.5*radius)
            for x in range(-radius+offset,width+radius,radius*3):
                points = [(x+radius*math.cos(math.radians(a)),y+radius*math.sin(math.radians(a))) for a in range(0,360,60)]
                draw.polygon(points, outline=mix(page,accent if (x//30+row)%5==0 else active,.4))
        draw.line((0,38,width-1,38), fill=accent, width=2)


def make_toolbar(theme, width=X20_SIZE[0]):
    _, _, _, _, _, style, _, _, palette = theme
    page, panel, accent, active = color(palette[8]), color(palette[5]), color(palette[2]), color(palette[10])
    height = X20_SIZE[1]
    image = Image.new("RGB", (width,height), page)
    draw = ImageDraw.Draw(image)
    gradient(draw, width, height, page, panel)

    def render_panel(panel_width, panel_height, side):
        flank = Image.new("RGB", (panel_width, panel_height), page)
        artwork(ImageDraw.Draw(flank), style, panel_width, panel_height,
                page, panel, accent, active, side)
        return flank

    image = compose_toolbar_sides(image, render_panel)
    draw = ImageDraw.Draw(image)
    draw.line((0,height-1,width-1,height-1), fill=mix(page,(0,0,0),.35))
    return image


def build_theme(theme):
    collection, slug, name, key, release_name, _, rounded, focus, palette = theme
    folder = f"theme-{slug}"
    theme_dir = THEMES_ROOT / folder
    large_name = f"toolbar-{slug}.png"
    small_name = f"toolbar-{slug}-x18.png"

    if theme_dir.exists(): shutil.rmtree(theme_dir)
    theme_dir.mkdir(parents=True)
    RELEASES_ROOT.mkdir(parents=True,exist_ok=True)

    for width, filename in ((X20_SIZE[0], large_name), (X18_SIZE[0], small_name)):
        save_png(make_toolbar(theme, width), theme_dir / filename)

    lines = []
    for index, role in enumerate(ROLES):
        lines.append(f"            {lua_rgb(palette[index])}, -- {role}")
    lines.insert(6,"            COLOR_BLACK, -- OVERLAY_COLOR")
    lines.append(f"            {lua_rgb(palette[8])}, -- TOPLCD_BGCOLOR")
    lua = f'''-- {name}
-- Standalone ETHOS radio theme. Rotorflight and RF Suite files are not modified.
{SELECTOR_LUA}local function init()
{INIT_GUARD_LUA}    system.registerTheme({{
        key = "{key}",
        name = "{name}",
        roundButtons = {str(rounded).lower()},
        focusStyle = "{focus}",
        colors = {{
{chr(10).join(lines)}
        }},
        toolbarBackground = {toolbar_call(large_name, small_name)},
    }})
end

return {{ init = init }}
'''
    (theme_dir/"main.lua").write_text(polish_lua_source(lua),encoding="utf-8",newline="\n")
    manifest = {
        "manifestVersion":1,"name":name,"key":f"mbwallace1390-theme-{key}","version":THEME_VERSION,
        "releaseNotes":{"format":"markdown","content":(f"{ETHOS26_RELEASE_NOTES} "
                f"First stable {name} release from the {collection} collection. Custom "
                    "radio-theme artwork only; no Rotorflight or RF Suite files are changed. "
                    "Automatically selects 464x50 artwork on standard X18 radios and 784x50 "
                    "artwork on 800px radios.")},
        "folder":folder,"files":["main.lua","toolbar-*"]
    }
    (theme_dir/"ethos_lua_manifest.json").write_text(json.dumps(manifest,indent=4)+"\n",encoding="utf-8",newline="\n")
    (theme_dir/"README.md").write_text(
        f"# {name} v{THEME_VERSION}\n\n{ETHOS26_SUPPORT}\n\n{zip_install_instructions(folder)}\n\n**Collection:** {collection}\n\nA standalone FrSky ETHOS radio theme with custom toolbar artwork.\n\n"
        f"- Focus: `{focus}`\n- Controls: {'rounded' if rounded else 'square'}\n- Internal key: `{key}`\n- Responsive 784x50 X20 / 464x50 X18 toolbar\n"
        "- Does not modify Rotorflight or RF Suite Lua files\n\n"
        f"To install from repository sources, copy `{folder}` into the transmitter `scripts` folder, restart, then select **{name}** under **System > General > Theme**.\n",
        encoding="utf-8",newline="\n")

    add_toolbar_logo(theme_dir, slug)
    write_release(theme_dir, RELEASES_ROOT/release_name)


def previews():
    from preview_lib import render_collection
    for slug, (title, themes) in COLLECTIONS.items():
        render_collection(slug, title, themes)


def main():
    keys,slugs,names,releases = ([theme[i] for theme in THEMES] for i in (3,1,2,4))
    if len(keys)!=len(set(keys)) or any(len(key)>7 for key in keys): raise SystemExit("Keys must be unique and <=7 characters")
    if len(slugs)!=len(set(slugs)) or len(names)!=len(set(names)) or len(releases)!=len(set(releases)): raise SystemExit("Duplicate theme metadata")
    for theme in THEMES: build_theme(theme)
    previews()
    print(f"Generated {len(THEMES)} separate themes and {len(COLLECTIONS)} collection previews")


if __name__ == "__main__": main()
