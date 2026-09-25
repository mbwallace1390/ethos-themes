"""Build America 250, both native-size toolbar images, and its catalog preview.

Original artwork is drawn here, with no downloaded logos or radio draw loops.
"""
from __future__ import annotations

import math
from PIL import Image, ImageDraw, ImageFont
from generate_readme_previews import parse_theme
from theme_lib import (
    PREVIEWS_ROOT, RELEASES_ROOT, THEMES_ROOT,
    X18_SIZE, X20_SIZE, mix, save_png, write_release, write_theme_files,
)

# Match the user's separate America 250 Rotorflight dashboard identity.
NAVY, PANEL = (4, 14, 31), (8, 24, 47)
IVORY, RED, GOLD = (240, 231, 207), (184, 48, 49), (216, 170, 78)
BLUE = (127, 169, 210)
SLUG = "america250"
VERSION = "1.2.1"

# Fixed five-column glyphs keep radio art crisp and independent of host fonts.
GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "5": ("11111", "10000", "10000", "11110", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
}


def pixel_text(draw, xy, text, scale, color):
    x, y = xy
    for letter in text:
        for row, line in enumerate(GLYPHS[letter]):
            for col, filled in enumerate(line):
                if filled == "1":
                    left, top = x + col * scale, y + row * scale
                    draw.rectangle((left, top, left + scale - 1, top + scale - 1), fill=color)
        x += 6 * scale


def star(draw, cx, cy, radius, color):
    # Alternating radii at 36-degree intervals form a five-point star.
    points = []
    for index in range(10):
        angle = -math.pi / 2 + index * math.pi / 5
        r = radius if index % 2 == 0 else radius * 0.42
        points.append((cx + math.cos(angle) * r, cy + math.sin(angle) * r))
    draw.polygon(points, fill=color)


def toolbar(width):
    image = Image.new("RGB", (width, 50), NAVY)
    draw = ImageDraw.Draw(image)
    center = width // 2
    for y in range(50):
        draw.line((0, y, width - 1, y), fill=mix(NAVY, PANEL, y / 70))
    # Subdued edge decoration avoids competing with native toolbar indicators.
    for row in range(3):
        for column in range(10):
            x = 10 + column * 17 + (8 if row % 2 else 0)
            if x < center - 137:
                star(draw, x, 9 + row * 13, 2.5, mix(NAVY, IVORY, 0.24))
    for index in range(6):
        y = 4 + index * 7
        draw.polygon(((center + 125, y + 3), (width - 1, y),
                      (width - 1, y + 4), (center + 125, y + 7)),
                     fill=mix(NAVY, RED if index % 2 == 0 else IVORY, 0.37))
    # Keep the inscription's pixel dimensions identical on both radio widths.
    emblem_x = center - 112
    for index in range(13):
        angle = -math.pi / 2 + index * 2 * math.pi / 13
        star(draw, emblem_x + math.cos(angle) * 18,
             24 + math.sin(angle) * 18, 2.2, GOLD)
    star(draw, emblem_x, 24, 9, IVORY)
    pixel_text(draw, (center - 77, 9), "AMERICA", 2, IVORY)
    pixel_text(draw, (center - 72, 30), "1776-2026", 1, GOLD)
    draw.line((center + 14, 9, center + 14, 37), fill=mix(NAVY, GOLD, 0.6))
    pixel_text(draw, (center + 27, 10), "250", 4, GOLD)
    draw.line((0, 48, width - 1, 48), fill=RED)
    draw.line((0, 49, width - 1, 49), fill=GOLD)
    return image


def palette():
    return [
        ("PRIMARY_COLOR", IVORY), ("SECONDARY_BGCOLOR", (27, 47, 72)),
        ("HIGHLIGHT_COLOR", GOLD), ("HIGHLIGHT_CONTRASTING_COLOR", NAVY),
        ("DISABLE_COLOR", (109, 124, 142)), ("PRIMARY_BGCOLOR", PANEL),
        ("OVERLAY_COLOR", None), ("SECONDARY_COLOR", (187, 207, 227)),
        ("SAFE_COLOR", (87, 221, 144)), ("PAGE_BGCOLOR", NAVY),
        ("ERROR_COLOR", (255, 96, 106)), ("ACTIVE_COLOR", (122, 182, 241)),
        ("INACTIVE_COLOR", (125, 144, 165)), ("BUTTON_BORDER_ACTIVE_COLOR", GOLD),
        ("BUTTON_BORDER_COLOR", (59, 79, 103)), ("WARNING_COLOR", (255, 198, 74)),
        ("SAFE_CONTRASTING_COLOR", (8, 28, 18)), ("TOPLCD_BGCOLOR", NAVY),
    ]


def preview():
    theme = parse_theme(SLUG)
    colors = theme["colors"]
    canvas = Image.new("RGB", (1200, 726), NAVY)
    draw = ImageDraw.Draw(canvas)
    # Pillow's embedded scalable font is portable across Windows and Linux.
    def font(size):
        return ImageFont.load_default(size=size)
    draw.rectangle((0, 0, 1199, 7), fill=RED)
    draw.text((58, 46), "COMMEMORATIVE COLLECTION", font=font(17), fill=GOLD)
    draw.text((54, 76), "AMERICA 250", font=font(70), fill=IVORY)
    draw.text((59, 166), "1776 - 2026  /  Stars, stripes & a little gold.", font=font(24), fill=BLUE)
    draw.text((930, 66), "ETHOS 26", font=font(24), fill=GOLD)
    draw.text((930, 102), "RADIO THEME", font=font(16), fill=IVORY)
    # Use actual generated art/palette; these control boxes are illustrative.
    draw.rounded_rectangle((58, 234, 886, 604), radius=16, fill=PANEL,
                           outline=colors["BUTTON_BORDER_COLOR"], width=2)
    with Image.open(theme["toolbar"]) as art:
        canvas.paste(art.convert("RGB"), (80, 256))
    draw.text((81, 332), "CONTROL PREVIEW", font=font(15), fill=BLUE)
    for index, label in enumerate(("Selected", "Normal", "Active", "Disabled")):
        x, y = 82 + index % 2 * 396, 367 + index // 2 * 106
        edge = GOLD if index in (0, 2) else colors["BUTTON_BORDER_COLOR"]
        text_color = (IVORY, IVORY, colors["ACTIVE_COLOR"], colors["DISABLE_COLOR"])[index]
        draw.rectangle((x, y, x + 370, y + 83), fill=NAVY, outline=edge,
                       width=3 if index == 0 else 1)
        star(draw, x + 33, y + 41, 9, text_color)
        draw.text((x + 59, y + 26), label, font=font(26), fill=text_color)
    draw.text((925, 242), "THE PALETTE", font=font(16), fill=GOLD)
    for index, (label, color) in enumerate((("Midnight navy", NAVY), ("Old-glory red", RED),
                                          ("Warm ivory", IVORY), ("Anniversary gold", GOLD))):
        y = 287 + index * 71
        draw.rounded_rectangle((925, y, 958, y + 33), radius=5, fill=color,
                               outline=colors["BUTTON_BORDER_COLOR"])
        draw.text((973, y + 7), label, font=font(17), fill=IVORY)
    draw.text((60, 640), "One download. Both display sizes.", font=font(23), fill=IVORY)
    draw.text((602, 646), "Gold focus | Square controls | Navy panels", font=font(17), fill=BLUE)
    draw.line((59, 678, 1141, 678), fill=colors["BUTTON_BORDER_COLOR"])
    draw.text((60, 696), "Actual toolbar artwork | Illustrative controls | Radio validation pending",
              font=font(14), fill=BLUE)
    PREVIEWS_ROOT.mkdir(parents=True, exist_ok=True)
    canvas.save(PREVIEWS_ROOT / "america250.png", optimize=True)


def main():
    theme_dir = THEMES_ROOT / "theme-america250"
    theme_dir.mkdir(parents=True, exist_ok=True)
    large, small = write_theme_files(
        theme_dir, name="America 250", key="USA250", family="Commemorative",
        label="Collection", slug=SLUG,
        header="America 250 anniversary theme. Native ETHOS radio theme; no background tasks.",
        round_buttons=False, focus_style="outline", roles=palette(),
        version=VERSION, hide_toolbar_logo=True,
        release_notes="Header fix: a transparent bitmap replaces the default ETHOS logo so America 250 stays readable. Navy, ivory, red and gold; 13-star medallion and 1776-2026 toolbar artwork.",
        readme_extra=("- Original commemorative artwork, drawn natively for both display sizes\n"
                      "- Default ETHOS header logo replaced with a transparent bitmap to keep the inscription visible\n"),
    )
    for width, name in ((X20_SIZE[0], large), (X18_SIZE[0], small)):
        save_png(toolbar(width), theme_dir / name)
    write_release(theme_dir, RELEASES_ROOT / f"America-250-v{VERSION}.zip")
    preview()
    print("Generated America 250: native X18/X20 artwork, Suite ZIP, and featured preview")


if __name__ == "__main__":
    main()
