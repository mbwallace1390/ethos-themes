"""Build Copperline, Stormfront, and Night Current as static native themes.

Artwork is authored independently at both native widths. All image processing
happens here on the desktop; the radio only loads its selected header and logo.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from theme_lib import (
    RELEASES_ROOT, THEMES_ROOT, X18_SIZE, X20_SIZE, mix, rgb, save_png,
    write_release, write_theme_files,
)

VERSION = "1.0.1"
FAMILY = "New Designs"
ART_SCALE = 3
STORM_SOURCE = Path(__file__).resolve().parent / "assets" / "stormfront" / "clouds-source.png"

# Colors: page, panel, secondary panel, foreground, focus, active, border.
THEMES = [
    {"slug": "copperline", "name": "Copperline", "key": "CprLine",
     "colors": ("15110F", "231E1A", "332B24", "F4E9DC", "D99357", "F1BD70", "5D4838"),
     "description": "Warm charcoal and copper with fine etched contours and concentric metal rings."},
    {"slug": "stormfront", "name": "Stormfront", "key": "Stormfr",
     "colors": ("08151F", "142A3A", "233B4B", "EAF4FF", "61BAFF", "B9E3FF", "355D72"),
     "description": "Cold slate and electric blue with layered storm clouds and lightning on both flanks."},
    {"slug": "night-current", "name": "Night Current", "key": "NtCurr",
     "colors": ("08141A", "10272E", "19353D", "E5F4F2", "50DBC3", "B9ECE6", "356A70"),
     "description": "Deep navy and pearl with flowing teal currents around the centered wordmark."},
]
SLUGS = tuple(theme["slug"] for theme in THEMES)


def palette(theme):
    page, panel, secondary, foreground, accent, active, border = map(rgb, theme["colors"])
    return [
        ("PRIMARY_COLOR", foreground),
        ("SECONDARY_BGCOLOR", secondary),
        ("HIGHLIGHT_COLOR", accent),
        ("HIGHLIGHT_CONTRASTING_COLOR", page),
        ("DISABLE_COLOR", mix(panel, foreground, .42)),
        ("PRIMARY_BGCOLOR", panel),
        ("OVERLAY_COLOR", None),
        ("SECONDARY_COLOR", mix(foreground, accent, .18)),
        ("SAFE_COLOR", rgb("68D594")),
        ("PAGE_BGCOLOR", page),
        ("ERROR_COLOR", rgb("F17F8F")),
        ("ACTIVE_COLOR", active),
        ("INACTIVE_COLOR", mix(panel, foreground, .55)),
        ("BUTTON_BORDER_ACTIVE_COLOR", active),
        ("BUTTON_BORDER_COLOR", border),
        ("WARNING_COLOR", rgb("EBC378")),
        ("SAFE_CONTRASTING_COLOR", rgb("081A10")),
        ("TOPLCD_BGCOLOR", panel),
    ]


def material(width, colors, *, metal=False):
    """One uninterrupted dark material; subtle grain remains under the logo."""
    page, panel = map(rgb, colors[:2])
    image = Image.new("RGB", (width, 50))
    pixels = image.load()
    for y in range(50):
        for x in range(width):
            shade = .12 + .21 * y / 49
            if metal:
                shade += .045 * math.sin(y * 2.1) + .02 * math.sin(x * .37 + y)
            else:
                shade += .035 * math.sin(x / 57 + y / 11)
            pixels[x, y] = mix(page, panel, shade)
    return image


def draw_scaled_line(draw, points, color, width=.65):
    draw.line([(round(x * ART_SCALE), round(y * ART_SCALE)) for x, y in points],
              fill=color, width=max(1, round(width * ART_SCALE)), joint="curve")


def copperline_toolbar(width, theme):
    """Fine copper engraving, with ring centers composed for the actual width."""
    base = material(width, theme["colors"], metal=True)
    accent = rgb(theme["colors"][4])
    layer = Image.new("RGBA", (width * ART_SCALE, 50 * ART_SCALE))
    draw = ImageDraw.Draw(layer)
    # The etched channels curve around the lettering rather than fading into
    # a rectangular center panel. Ring-to-channel transitions stay subdued.
    ring_x = 20 if width == 464 else 34
    for side in (-1, 1):
        for index in range(17):
            points = []
            for x in range(width):
                distance = abs(x - (width - 1) / 2)
                route = math.exp(-((distance / 112) ** 4))
                wave = (8.0 * math.sin(x * math.pi * 4 / width + index * .13)
                        + 3 * math.sin(x * math.pi * 7 / width))
                y = 25 + side * (2 + index * 2.25 + 17.5 * route) + wave * (1 - .8 * route)
                points.append((x, y))
            shade = .43 + .18 * math.sin(index * 1.67) ** 2
            draw_scaled_line(draw, points, (*mix(rgb("34251A"), accent, shade), 185), .55)
    # Dense concentric rings create the fingerprint-like metal focal points.
    for cx in (ring_x, width - 1 - ring_x):
        for index in range(20):
            radius = 3.5 + index * 3.1
            box = [(cx - radius) * ART_SCALE, (25 - radius * .78) * ART_SCALE,
                   (cx + radius) * ART_SCALE, (25 + radius * .78) * ART_SCALE]
            shade = .50 + .36 * math.sin(index * 1.1) ** 2
            draw.ellipse(box, outline=(*mix(rgb("38291D"), accent, shade), 240), width=2)
    layer = layer.resize(base.size, Image.Resampling.LANCZOS)
    glow = layer.filter(ImageFilter.GaussianBlur(.65))
    glow.putalpha(glow.getchannel("A").point(lambda value: round(value * .22)))
    return Image.alpha_composite(Image.alpha_composite(base.convert("RGBA"), glow), layer).convert("RGB")


def night_current_toolbar(width, theme):
    """Layered fluid filaments remain connected through the full-width scene."""
    base = material(width, theme["colors"])
    accent = rgb(theme["colors"][4])
    layer = Image.new("RGBA", (width * ART_SCALE, 50 * ART_SCALE))
    draw = ImageDraw.Draw(layer)
    # Narrow currents sweep up/down beside the center. The wide outer curves
    # pass above/below the letters, keeping their luminous cores out of the logo.
    for side in (-1, 1):
        for index in range(18):
            points = []
            for x in range(width):
                distance = abs(x - (width - 1) / 2)
                route = math.exp(-((distance / 119) ** 4))
                wave = (17 * math.sin(4 * math.pi * x / width + .25)
                        + 7 * math.sin(7 * math.pi * x / width + index * .12))
                y = 25 + side * (1 + index * 2.0 + 19.5 * route) + wave * (1 - .88 * route)
                points.append((x, y))
            strength = .38 + .55 * math.sin(index * 1.9) ** 2
            color = mix(rgb("0D4F57"), accent, strength)
            draw_scaled_line(draw, points, (*color, 210), .55 if index % 4 else .85)
    layer = layer.resize(base.size, Image.Resampling.LANCZOS)
    glow = layer.filter(ImageFilter.GaussianBlur(.8))
    glow.putalpha(glow.getchannel("A").point(lambda value: round(value * .23)))
    return Image.alpha_composite(Image.alpha_composite(base.convert("RGBA"), glow), layer).convert("RGB")


def stormfront_toolbar(width, theme):
    if not STORM_SOURCE.is_file():
        raise FileNotFoundError(f"Missing Stormfront scene source: {STORM_SOURCE}")
    with Image.open(STORM_SOURCE) as source:
        # Use the entire cloud panorama and change the vertical field of view
        # for each native aspect ratio. No stretching or X20-to-X18 resampling.
        source = source.convert("RGB")
        crop_height = round(source.width * 50 / width)
        center_y = round(source.height * .456)
        top = min(source.height - crop_height, max(0, center_y - crop_height // 2))
        base = source.crop((0, top, source.width, top + crop_height)).resize(
            (width, 50), Image.Resampling.LANCZOS)

    bolt_layer = Image.new("RGBA", (width * ART_SCALE, 50 * ART_SCALE))
    bolts = ImageDraw.Draw(bolt_layer)
    for fraction, direction in ((.16, 1), (.84, -1)):
        cx = round(width * fraction)
        # Fixed native-size geometry keeps the branching flash recognizable on
        # either radio, well outside the centered128px lettering footprint.
        trunk = [(cx - 4 * direction, 1), (cx + direction, 7),
                 (cx - 2 * direction, 12), (cx + 4 * direction, 19),
                 (cx + direction, 23), (cx + 7 * direction, 31),
                 (cx + 4 * direction, 36), (cx + 11 * direction, 48)]
        branches = [
            [(cx + 4 * direction, 19), (cx - 6 * direction, 23),
             (cx - 8 * direction, 30), (cx - 15 * direction, 34),
             (cx - 19 * direction, 43)],
            [(cx + 7 * direction, 31), (cx + 16 * direction, 33),
             (cx + 20 * direction, 40), (cx + 26 * direction, 44)],
            [(cx + direction, 7), (cx + 8 * direction, 12),
             (cx + 13 * direction, 12), (cx + 18 * direction, 17)],
        ]
        for path in branches:
            draw_scaled_line(bolts, path, (116, 195, 255, 225), .55)
        draw_scaled_line(bolts, trunk, (204, 235, 255, 255), .8)
    bolt_layer = bolt_layer.resize(base.size, Image.Resampling.LANCZOS)
    glow = bolt_layer.filter(ImageFilter.GaussianBlur(1.0))
    glow.putalpha(glow.getchannel("A").point(lambda value: min(255, round(value * 1.6))))
    return Image.alpha_composite(Image.alpha_composite(base.convert("RGBA"), glow), bolt_layer).convert("RGB")


RENDERERS = {
    "copperline": copperline_toolbar,
    "stormfront": stormfront_toolbar,
    "night-current": night_current_toolbar,
}


def build(theme):
    slug = theme["slug"]
    if slug not in SLUGS:
        raise ValueError(f"Unknown theme: {slug}")
    folder = THEMES_ROOT / f"theme-{slug}"
    # Only known files in these three folders are written; preserve any other
    # files a developer has placed alongside them instead of deleting a tree.
    if folder.resolve().parent != THEMES_ROOT.resolve():
        raise ValueError(f"Theme folder is outside the catalog: {folder}")
    folder.mkdir(parents=True, exist_ok=True)
    large_name, small_name = write_theme_files(
        folder, name=theme["name"], key=theme["key"], family=FAMILY,
        slug=slug, header="Standalone ETHOS radio theme with static native artwork.",
        round_buttons=True, focus_style="outline", roles=palette(theme),
        version=VERSION, release_notes=f"First release. {theme['description']}",
        readme_extra=(f"- {theme['description']}\n"
                      "- Static artwork with no recurring Lua drawing or telemetry work\n"),
    )
    for width, filename in ((X20_SIZE[0], large_name), (X18_SIZE[0], small_name)):
        save_png(RENDERERS[slug](width, theme), folder / filename)
    release_name = "-".join(theme["name"].split()) + f"-v{VERSION}.zip"
    write_release(folder, RELEASES_ROOT / release_name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slugs", nargs="+", choices=SLUGS, default=SLUGS)
    args = parser.parse_args()
    selected = [theme for theme in THEMES if theme["slug"] in args.slugs]
    for theme in selected:
        build(theme)
    if set(args.slugs) == set(SLUGS):
        from preview_lib import render_collection
        render_collection("new-designs", FAMILY, SLUGS)
    print(f"Generated {len(selected)} native ETHOS themes, version {VERSION}")


if __name__ == "__main__":
    main()
