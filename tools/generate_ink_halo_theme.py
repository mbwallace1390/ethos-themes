"""Build Ink & Halo with portable original artwork and a source-driven preview.

The glow is baked into native-size opaque PNGs; the radio does no animation or
background drawing. Fixed glyphs keep the installed art independent of fonts.
"""
from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageFont

from preview_lib import parse_theme
from theme_lib import (
    PREVIEWS_ROOT, RELEASES_ROOT, THEMES_ROOT, X18_SIZE, X20_SIZE,
    mix, save_png, write_release, write_theme_files,
)

INK = (8, 11, 16)
PANEL = (13, 16, 23)
WHITE = (244, 247, 252)
ICE = (189, 215, 255)
SLUG = "ink-halo"
VERSION = "1.0.0"

# Five-column, seven-row glyphs render a small, deliberately spaced inscription.
GLYPHS = {
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "N": ("10001", "11001", "11001", "10101", "10011", "10011", "10001"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    " ": ("00000",) * 7,
}


def pixel_text(draw, center_x, y, text, color):
    """Keep the label at the same pixel size on both display widths."""
    scale = 2
    width = (len(text) * 8 - 3) * scale
    x = center_x - width // 2
    for letter in text:
        for row, line in enumerate(GLYPHS[letter]):
            for column, filled in enumerate(line):
                if filled == "1":
                    left, top = x + column * scale, y + row * scale
                    draw.rectangle((left, top, left + scale - 1, top + scale - 1), fill=color)
        x += 8 * scale


def toolbar(width):
    """Draw a luminous elliptical horizon while leaving both ends quiet."""
    image = Image.new("RGB", (width, 50), INK)
    pixels = image.load()
    center = (width - 1) / 2
    visible_half_width = min(194.0, width * 0.285)
    center_y, radius_y = 170.0, 166.0
    # Solve the ellipse radius so the arc exits through the bottom of the strip.
    radius_x = visible_half_width / math.sqrt(1 - ((center_y - 50) / radius_y) ** 2)
    for x in range(width):
        relative_x = (x - center) / radius_x
        arc_y = (center_y - radius_y * math.sqrt(1 - relative_x * relative_x)
                 if abs(relative_x) < 1 else 1000.0)
        tint = mix(ICE, WHITE, max(0.0, min(1.0, 0.55 + relative_x * 0.55)))
        for y in range(50):
            distance = y - arc_y
            # Three finite Gaussian bands bake antialiasing and light bloom in.
            strength = min(1.0, 0.19 * math.exp(-(distance / 6.4) ** 2)
                           + 0.24 * math.exp(-(distance / 1.9) ** 2)
                           + 0.76 * math.exp(-(distance / 0.62) ** 2))
            pixels[x, y] = mix(mix(INK, PANEL, y / 100), tint, strength)
    draw = ImageDraw.Draw(image)
    pixel_text(draw, width // 2, 28, "INK & HALO", WHITE)
    draw.line((0, 49, width - 1, 49), fill=(40, 49, 63))
    return image


def palette():
    return [
        ("PRIMARY_COLOR", WHITE), ("SECONDARY_BGCOLOR", (23, 29, 40)),
        ("HIGHLIGHT_COLOR", ICE), ("HIGHLIGHT_CONTRASTING_COLOR", INK),
        ("DISABLE_COLOR", (116, 127, 145)), ("PRIMARY_BGCOLOR", PANEL),
        ("OVERLAY_COLOR", None), ("SECONDARY_COLOR", (181, 191, 206)),
        ("SAFE_COLOR", (141, 201, 164)), ("PAGE_BGCOLOR", INK),
        ("ERROR_COLOR", (242, 147, 156)), ("ACTIVE_COLOR", ICE),
        ("INACTIVE_COLOR", (152, 163, 181)), ("BUTTON_BORDER_ACTIVE_COLOR", ICE),
        ("BUTTON_BORDER_COLOR", (84, 100, 122)), ("WARNING_COLOR", (230, 199, 134)),
        ("SAFE_CONTRASTING_COLOR", INK), ("TOPLCD_BGCOLOR", PANEL),
    ]


def preview():
    """Show actual palette/art and clearly labelled illustrative native controls."""
    theme = parse_theme(SLUG)
    colors = theme["colors"]
    page = colors["PAGE_BGCOLOR"]
    panel = colors["PRIMARY_BGCOLOR"]
    text = colors["PRIMARY_COLOR"]
    accent = colors["HIGHLIGHT_COLOR"]
    secondary = colors["SECONDARY_COLOR"]
    border = colors["BUTTON_BORDER_COLOR"]
    canvas = Image.new("RGB", (1200, 804), page)
    draw = ImageDraw.Draw(canvas)

    def font(size):
        return ImageFont.load_default(size=size)

    draw.text((57, 39), "SIGNATURE COLLECTION", font=font(16), fill=accent)
    draw.text((52, 73), "INK & HALO", font=font(68), fill=text)
    draw.text((58, 160), "Dark ink. A quiet glow.", font=font(25), fill=secondary)
    draw.text((953, 63), "ETHOS 26", font=font(23), fill=accent)
    draw.text((953, 99), "RADIO THEME", font=font(15), fill=text)

    # Paste the installed 784 x 50 image without resizing it.
    draw.rounded_rectangle((58, 224, 886, 612), radius=16, fill=panel,
                           outline=border, width=2)
    with Image.open(theme["toolbar"]) as art:
        canvas.paste(art.convert("RGB"), (80, 246))
    draw.text((81, 321), "CONTROL PREVIEW", font=font(14), fill=secondary)
    for index, label in enumerate(("Selected", "Normal", "Active", "Disabled")):
        x = 82 + index % 2 * 396
        y = 355 + index // 2 * 88
        edge = accent if index in (0, 2) else border
        foreground = (text, text, colors["ACTIVE_COLOR"], colors["DISABLE_COLOR"])[index]
        bounds = (x, y, x + 370, y + 70)
        draw.rounded_rectangle(bounds, radius=10, fill=page, outline=edge,
                               width=3 if index == 0 else 1)
        draw.ellipse((x + 25, y + 27, x + 39, y + 41), outline=foreground, width=2)
        draw.text((x + 57, y + 22), label, font=font(24), fill=foreground)
    draw.rounded_rectangle((82, 540, 851, 588), radius=8,
                           fill=colors["SECONDARY_BGCOLOR"], outline=border)
    draw.text((101, 554), "Theme", font=font(18), fill=secondary)
    draw.rounded_rectangle((429, 547, 844, 581), radius=6, fill=accent)
    draw.text((447, 554), theme["name"], font=font(18),
              fill=colors["HIGHLIGHT_CONTRASTING_COLOR"])
    draw.polygon(((818, 559), (830, 559), (824, 565)),
                 fill=colors["HIGHLIGHT_CONTRASTING_COLOR"])

    draw.text((927, 233), "THE PALETTE", font=font(15), fill=accent)
    for index, (label, role) in enumerate((("Ink", "PAGE_BGCOLOR"),
                                          ("Panel", "PRIMARY_BGCOLOR"),
                                          ("Soft white", "PRIMARY_COLOR"),
                                          ("Halo blue", "HIGHLIGHT_COLOR"))):
        y = 276 + index * 78
        color = colors[role]
        draw.rounded_rectangle((927, y, 960, y + 33), radius=6, fill=color, outline=border)
        draw.text((975, y), label, font=font(18), fill=text)
        draw.text((975, y + 25), "#" + "".join(f"{channel:02X}" for channel in color),
                  font=font(13), fill=secondary)
    draw.text((60, 643), "NATIVE X18 ARTWORK  /  464 x 50", font=font(15), fill=secondary)
    with Image.open(THEMES_ROOT / "theme-ink-halo" / "toolbar-ink-halo-x18.png") as art:
        canvas.paste(art.convert("RGB"), (60, 677))
    draw.text((600, 648), "One download. Both display sizes.", font=font(22), fill=text)
    draw.text((600, 686), "Halo focus | Rounded controls | Ink panels", font=font(17), fill=secondary)
    draw.line((59, 754, 1141, 754), fill=border)
    draw.text((60, 774), "Actual toolbar artwork | Illustrative controls | Radio validation pending",
              font=font(14), fill=secondary)
    PREVIEWS_ROOT.mkdir(parents=True, exist_ok=True)
    canvas.save(PREVIEWS_ROOT / "ink-halo.png", optimize=True)


def main():
    theme_dir = THEMES_ROOT / "theme-ink-halo"
    theme_dir.mkdir(parents=True, exist_ok=True)
    large, small = write_theme_files(
        theme_dir, name="Ink & Halo", key="INKHALO", family="Signature",
        label="Collection", slug=SLUG,
        header="Ink-black panels and a quiet halo. Native ETHOS radio theme; no background tasks.",
        round_buttons=True, focus_style="outline", roles=palette(),
        version=VERSION, hide_toolbar_logo=True,
        release_notes=("Initial Ink & Halo release: ink-black panels, soft-white text, "
                       "pale-blue focus borders, rounded controls, and an original luminous halo header."),
        readme_extra=("- Original halo artwork, drawn at each native display width\n"
                      "- Glow is baked into opaque PNGs; no animation or background drawing\n"
                      "- Transparent logo override keeps the centered Ink & Halo inscription clear\n"),
    )
    for width, name in ((X20_SIZE[0], large), (X18_SIZE[0], small)):
        save_png(toolbar(width), theme_dir / name)
    write_release(theme_dir, RELEASES_ROOT / f"Ink-and-Halo-v{VERSION}.zip")
    preview()
    print("Generated Ink & Halo: native X18/X20 artwork, Suite ZIP, and catalog preview")


if __name__ == "__main__":
    main()
