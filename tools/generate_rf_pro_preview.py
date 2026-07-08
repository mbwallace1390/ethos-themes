from __future__ import annotations

import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
THEMES_ROOT = ROOT / "themes"
PREVIEWS_ROOT = ROOT / "previews"

THEMES = [
    "rfblue-pro",
    "rf-violet-pro",
    "rf-emerald-pro",
    "rf-ember-pro",
    "rf-magenta-pro",
    "rf-cyan-pro",
    "rf-crimson-pro",
    "rf-gold-pro",
    "rf-teal-pro",
    "rf-lime-pro",
]

ROLE_RE = re.compile(
    r"lcd\.RGB\(0x([0-9A-Fa-f]{2}),\s*0x([0-9A-Fa-f]{2}),\s*0x([0-9A-Fa-f]{2})\),\s*--\s*([A-Z_]+)"
)
NAME_RE = re.compile(r'name\s*=\s*"([^"]+)"')


def load_font(size: int, bold: bool = False):
    path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


TITLE_FONT = load_font(27, True)
NAME_FONT = load_font(14, True)
LABEL_FONT = load_font(11)
SMALL_FONT = load_font(12)


def parse_theme(slug: str) -> dict:
    folder = THEMES_ROOT / f"theme-{slug}"
    source = (folder / "main.lua").read_text(encoding="utf-8")
    colors = {
        role: (int(red, 16), int(green, 16), int(blue, 16))
        for red, green, blue, role in ROLE_RE.findall(source)
    }
    name_match = NAME_RE.search(source)
    toolbar_files = sorted(folder.glob("toolbar-*.png"))
    if not name_match or len(toolbar_files) != 1:
        raise ValueError(f"Could not parse {folder}")
    return {"name": name_match.group(1), "colors": colors, "toolbar": toolbar_files[0]}


def draw_card(canvas: Image.Image, draw: ImageDraw.ImageDraw, theme: dict, x: int, y: int) -> None:
    width, height = 226, 146
    colors = theme["colors"]
    page = colors["PAGE_BGCOLOR"]
    panel = colors["PRIMARY_BGCOLOR"]
    text = colors["PRIMARY_COLOR"]
    accent = colors["HIGHLIGHT_COLOR"]
    border = colors["BUTTON_BORDER_COLOR"]
    disabled = colors["DISABLE_COLOR"]

    draw.rounded_rectangle((x, y, x + width, y + height), radius=10, fill=page, outline=border, width=2)
    draw.text((x + 12, y + 10), theme["name"], font=NAME_FONT, fill=text)

    toolbar = Image.open(theme["toolbar"]).convert("RGB")
    toolbar = toolbar.resize((width - 24, 14), Image.Resampling.LANCZOS)
    canvas.paste(toolbar, (x + 12, y + 36))

    draw.rectangle((x + 12, y + 68, x + 104, y + 107), fill=panel, outline=accent, width=4)
    draw.text((x + 30, y + 82), "Selected", font=LABEL_FONT, fill=text)

    draw.rectangle((x + 122, y + 68, x + width - 12, y + 107), fill=panel, outline=border, width=2)
    draw.text((x + 144, y + 82), "Normal", font=LABEL_FONT, fill=text)

    draw.text((x + 12, y + 121), "Inactive", font=LABEL_FONT, fill=disabled)
    draw.line((x + 73, y + 130, x + width - 12, y + 130), fill=accent, width=2)


def main() -> None:
    themes = [parse_theme(slug) for slug in THEMES]
    columns = 3
    rows = (len(themes) + columns - 1) // columns
    width = 760
    height = 82 + rows * 160
    canvas = Image.new("RGB", (width, height), (8, 11, 17))
    draw = ImageDraw.Draw(canvas)
    draw.text((30, 18), "RF Pro Color Collection", font=TITLE_FONT, fill=(244, 247, 251))
    draw.text((30, 54), "Ten outline-focus color variants — click the image in the README for full size", font=SMALL_FONT, fill=(175, 189, 207))

    for index, theme in enumerate(themes):
        x = 30 + (index % columns) * 240
        y = 82 + (index // columns) * 160
        draw_card(canvas, draw, theme, x, y)

    PREVIEWS_ROOT.mkdir(parents=True, exist_ok=True)
    output = PREVIEWS_ROOT / "rf-pro.png"
    canvas.save(output, optimize=True)
    print(f"Generated {output}")


if __name__ == "__main__":
    main()
