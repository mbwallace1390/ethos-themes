from __future__ import annotations

import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
THEMES_ROOT = ROOT / "themes"
PREVIEWS_ROOT = ROOT / "previews"

FAMILIES = {
    "retro-instrument": (
        "Retro Instrument",
        ["amber-instrument", "phosphor-green", "ice-instrument"],
    ),
    "soft": (
        "Soft",
        ["soft-lavender", "soft-mint", "soft-coral", "soft-sky"],
    ),
    "oled-stealth": (
        "OLED Stealth",
        ["oled-blue", "oled-red", "oled-green", "oled-white"],
    ),
    "daylight": (
        "Daylight",
        ["daylight-blue", "daylight-orange", "daylight-green"],
    ),
    "industrial": (
        "Industrial",
        ["carbon", "gunmetal", "hazard", "titanium"],
    ),
    "two-tone": (
        "Two-Tone",
        ["violet-circuit", "blue-vector", "ember-signal", "neon-fusion"],
    ),
}

ROLE_RE = re.compile(
    r"lcd\.RGB\(0x([0-9A-Fa-f]{2}),\s*0x([0-9A-Fa-f]{2}),\s*0x([0-9A-Fa-f]{2})\),\s*--\s*([A-Z_]+)"
)
NAME_RE = re.compile(r'name\s*=\s*"([^"]+)"')
ROUND_RE = re.compile(r"roundButtons\s*=\s*(true|false)")
FOCUS_RE = re.compile(r'focusStyle\s*=\s*"([^"]+)"')


def font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


TITLE_FONT = font(27, True)
NAME_FONT = font(17, True)
LABEL_FONT = font(13)
SMALL_FONT = font(12)


def parse_theme(slug: str) -> dict:
    folder = THEMES_ROOT / f"theme-{slug}"
    lua_path = folder / "main.lua"
    source = lua_path.read_text(encoding="utf-8")

    colors = {}
    for red, green, blue, role in ROLE_RE.findall(source):
        colors[role] = (int(red, 16), int(green, 16), int(blue, 16))

    name_match = NAME_RE.search(source)
    round_match = ROUND_RE.search(source)
    focus_match = FOCUS_RE.search(source)
    if not name_match or not round_match or not focus_match:
        raise ValueError(f"Could not parse theme metadata from {lua_path}")

    toolbar_files = sorted(folder.glob("toolbar-*.png"))
    if len(toolbar_files) != 1:
        raise ValueError(f"Expected one toolbar PNG in {folder}")

    required = {
        "PRIMARY_COLOR",
        "HIGHLIGHT_COLOR",
        "HIGHLIGHT_CONTRASTING_COLOR",
        "DISABLE_COLOR",
        "PRIMARY_BGCOLOR",
        "ACTIVE_COLOR",
        "BUTTON_BORDER_ACTIVE_COLOR",
        "BUTTON_BORDER_COLOR",
        "PAGE_BGCOLOR",
    }
    missing = required - colors.keys()
    if missing:
        raise ValueError(f"Missing colors in {lua_path}: {sorted(missing)}")

    return {
        "name": name_match.group(1),
        "round": round_match.group(1) == "true",
        "focus": focus_match.group(1),
        "colors": colors,
        "toolbar": toolbar_files[0],
    }


def draw_card(canvas: Image.Image, draw: ImageDraw.ImageDraw, theme: dict, x: int, y: int) -> None:
    width, height = 340, 204
    colors = theme["colors"]
    page = colors["PAGE_BGCOLOR"]
    panel = colors["PRIMARY_BGCOLOR"]
    text = colors["PRIMARY_COLOR"]
    accent = colors["HIGHLIGHT_COLOR"]
    active = colors["ACTIVE_COLOR"]
    border = colors["BUTTON_BORDER_COLOR"]
    active_border = colors["BUTTON_BORDER_ACTIVE_COLOR"]
    disabled = colors["DISABLE_COLOR"]
    radius = 9 if theme["round"] else 0

    draw.rounded_rectangle((x, y, x + width, y + height), radius=12, fill=page, outline=border, width=2)
    draw.text((x + 15, y + 12), theme["name"], font=NAME_FONT, fill=text)
    draw.text((x + width - 88, y + 16), theme["focus"], font=SMALL_FONT, fill=disabled)

    toolbar = Image.open(theme["toolbar"]).convert("RGB")
    toolbar = toolbar.resize((width - 30, 20), Image.Resampling.LANCZOS)
    canvas.paste(toolbar, (x + 15, y + 43))

    selected_box = (x + 15, y + 82, x + 150, y + 137)
    normal_box = (x + 175, y + 82, x + width - 15, y + 137)

    if theme["focus"] == "invert":
        selected_fill = accent
        selected_outline = accent
        selected_text = colors["HIGHLIGHT_CONTRASTING_COLOR"]
    else:
        selected_fill = panel
        selected_outline = accent
        selected_text = text

    draw.rounded_rectangle(selected_box, radius=radius, fill=selected_fill, outline=selected_outline, width=4)
    draw.text((x + 47, y + 102), "Selected", font=LABEL_FONT, fill=selected_text)

    draw.rounded_rectangle(normal_box, radius=radius, fill=panel, outline=border, width=2)
    draw.text((x + 219, y + 102), "Normal", font=LABEL_FONT, fill=text)

    draw.rounded_rectangle((x + 15, y + 153, x + 150, y + 190), radius=radius, fill=panel, outline=active_border, width=2)
    draw.text((x + 57, y + 164), "Active", font=LABEL_FONT, fill=active)

    draw.rounded_rectangle((x + 175, y + 153, x + width - 15, y + 190), radius=radius, fill=panel, outline=border, width=2)
    draw.text((x + 211, y + 164), "Disabled", font=LABEL_FONT, fill=disabled)


def generate_family(slug: str, title: str, theme_slugs: list[str]) -> None:
    themes = [parse_theme(theme_slug) for theme_slug in theme_slugs]
    rows = (len(themes) + 1) // 2
    width = 760
    height = 82 + rows * 226
    canvas = Image.new("RGB", (width, height), (8, 11, 17))
    draw = ImageDraw.Draw(canvas)
    draw.text((30, 18), title, font=TITLE_FONT, fill=(244, 247, 251))
    draw.text((30, 54), "Theme family preview — click the image in the README for full size", font=SMALL_FONT, fill=(175, 189, 207))

    for index, theme in enumerate(themes):
        x = 30 + (index % 2) * 370
        y = 82 + (index // 2) * 226
        draw_card(canvas, draw, theme, x, y)

    PREVIEWS_ROOT.mkdir(parents=True, exist_ok=True)
    canvas.save(PREVIEWS_ROOT / f"{slug}.png", optimize=True)


if __name__ == "__main__":
    for family_slug, (title, theme_slugs) in FAMILIES.items():
        generate_family(family_slug, title, theme_slugs)
    print(f"Generated {len(FAMILIES)} README preview images in {PREVIEWS_ROOT}")
