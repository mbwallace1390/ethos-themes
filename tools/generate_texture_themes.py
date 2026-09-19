"""Build the Texture collection.

Four standalone themes built from surface textures rather than scenery: an
over-under basket weave, jittered stained-glass cells, a halftone dot screen,
and soft overlapping bokeh orbs.

Like the Elements collection the artwork is rendered natively at both display
widths, so the dot screen and weave stay aligned to the pixel grid on a 480px
X18 instead of being smeared by a resample.
"""

from __future__ import annotations

import math
import random
import shutil

from PIL import Image, ImageChops, ImageDraw

from theme_lib import (
    RELEASES_ROOT,
    THEMES_ROOT,
    THEME_VERSION,
    X18_SIZE,
    X20_SIZE,
    contrasting,
    mix,
    rgb,
    save_png,
    write_release,
    write_theme_files,
)

# slug, name, key, style, accent (focus), active, page, panel, seed
THEMES = [
    ("loom", "Loom", "Loom", "weave", "#E0864A", "#FFC98A", "#100C09", "#241A13", 611),
    ("mosaic", "Mosaic", "Mosaic", "mosaic", "#2FC7A8", "#FFC94A", "#06110F", "#0D2320", 612),
    ("halftone", "Halftone", "Halftn", "halftone", "#FF4D5E", "#FFB020", "#0B0B0C", "#1C1C1F", 613),
    ("bloom", "Bloom", "Bloom", "bloom", "#FF6FB5", "#A98CFF", "#0C0812", "#1E1430", 614),
]

DESCRIPTIONS = {
    "loom": "an over-under basket weave in warm rust and amber",
    "mosaic": "jittered stained-glass cells with lit seams",
    "halftone": "a halftone dot screen that swells and fades across the bar",
    "bloom": "soft overlapping bokeh orbs in pink and violet",
}


def weave(image, draw, w, h, page, panel, accent, active, rng):
    """Over-under basket weave.

    Both strand directions are laid down solid first so each reads as
    continuous, then the vertical strands are redrawn on alternating cells to
    put them back on top — which is what makes the interlace legible.
    """
    cell, strand = 12, 8
    warp = mix(panel, accent, 0.44)
    weft = mix(panel, active, 0.20)
    shade = mix(panel, (0, 0, 0), 0.34)

    def vertical(x0, y0, y1):
        draw.rectangle((x0, y0, x0 + strand - 1, y1), fill=weft)
        draw.line((x0, y0, x0, y1), fill=shade)
        draw.line((x0 + strand - 1, y0, x0 + strand - 1, y1), fill=shade)

    for x in range(-cell, w + cell, cell):
        vertical(x + 2, 0, h - 1)

    for y in range(-cell, h + cell, cell):
        top = y + 2
        draw.rectangle((0, top, w - 1, top + strand - 1), fill=warp)
        draw.line((0, top, w - 1, top), fill=shade)
        draw.line((0, top + strand - 1, w - 1, top + strand - 1), fill=shade)

    for row_index, y in enumerate(range(-cell, h + cell, cell)):
        for col_index, x in enumerate(range(-cell, w + cell, cell)):
            if (row_index + col_index) % 2 == 0:
                vertical(x + 2, y, y + cell - 1)


def mosaic(image, draw, w, h, page, panel, accent, active, rng):
    """Stained-glass cells from a jittered grid, edges pushed past the border."""
    rows, cols = 3, max(6, w // 30)
    cell_w, cell_h = w / cols, h / rows
    points = []
    for r in range(rows + 1):
        row = []
        for c in range(cols + 1):
            x = c * cell_w + rng.uniform(-cell_w * 0.22, cell_w * 0.22)
            y = r * cell_h + rng.uniform(-cell_h * 0.26, cell_h * 0.26)
            # Anchor the outer ring outside the canvas so no background shows.
            if c == 0:
                x = -3
            elif c == cols:
                x = w + 3
            if r == 0:
                y = -3
            elif r == rows:
                y = h + 3
            row.append((x, y))
        points.append(row)

    seam = mix(page, active, 0.40)
    for r in range(rows):
        for c in range(cols):
            quad = [points[r][c], points[r][c + 1], points[r + 1][c + 1], points[r + 1][c]]
            hue = accent if rng.random() < 0.62 else active
            draw.polygon(quad, fill=mix(panel, hue, 0.14 + rng.random() * 0.42), outline=seam)


def halftone(image, draw, w, h, page, panel, accent, active, rng):
    """Offset dot screen whose radius rides a slow wave across the bar."""
    step = 8
    for row_index, y in enumerate(range(3, h, step)):
        offset = (row_index % 2) * (step // 2)
        for x in range(3 + offset, w, step):
            amount = 0.5 + 0.5 * math.sin((x / w) * 5.2 + row_index * 0.55)
            radius = 0.8 + amount * 2.4
            hue = accent if amount > 0.5 else active
            draw.ellipse(
                (x - radius, y - radius, x + radius, y + radius),
                fill=mix(panel, hue, 0.22 + amount * 0.55),
            )


def bloom(image, draw, w, h, page, panel, accent, active, rng):
    """Soft bokeh orbs.

    Each orb is accumulated into a grayscale mask so overlaps brighten instead
    of painting over one another, then the two masks tint the background.
    """
    masks = {"accent": Image.new("L", (w, h), 0), "active": Image.new("L", (w, h), 0)}

    for _ in range(max(8, w // 26)):
        radius = rng.randint(7, 18)
        centre_x, centre_y = rng.randrange(w), rng.randint(4, h - 6)
        # Move complete bright orbs aside rather than blanking part of their glow.
        clearance = 72 + radius
        if abs(centre_x - (w - 1) / 2) < clearance:
            outer_x = rng.randint(radius, int((w - 1) / 2 - clearance))
            centre_x = outer_x if centre_x < w / 2 else w - 1 - outer_x
        span = radius * 2
        patch = Image.new("L", (span, span), 0)
        pixels = patch.load()
        for py in range(span):
            for px in range(span):
                distance = math.hypot(px - radius + 0.5, py - radius + 0.5) / radius
                if distance < 1.0:
                    pixels[px, py] = int(255 * (1 - distance) ** 1.9)
        layer = Image.new("L", (w, h), 0)
        layer.paste(patch, (centre_x - radius, centre_y - radius))
        key = "accent" if rng.random() < 0.55 else "active"
        masks[key] = ImageChops.add(masks[key], layer)

    result = Image.composite(Image.new("RGB", (w, h), accent), image.copy(), masks["accent"])
    result = Image.composite(Image.new("RGB", (w, h), active), result, masks["active"])
    image.paste(result, (0, 0))


STYLES = {"weave": weave, "mosaic": mosaic, "halftone": halftone, "bloom": bloom}


def toolbar(width, style, page, panel, accent, active, seed) -> Image.Image:
    height = X20_SIZE[1]
    image = Image.new("RGB", (width, height), page)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        draw.line((0, y, width - 1, y), fill=mix(page, panel, (y / (height - 1)) * 0.85))
    base = image.copy()
    STYLES[style](image, draw, width, height, page, panel, accent, active, random.Random(seed))
    if style != "bloom":
        pixels, background = image.load(), base.load()
        # A soft oval reduces contrast beneath the letters, retaining at least
        # 60% of every strand, cell and dot instead of cutting a rectangular gap.
        for y in range(height):
            for x in range(width):
                distance = ((x - (width - 1) / 2) / 110) ** 2 + ((y - 26) / 24) ** 2
                quieten = max(0.0, 1 - distance) ** 2 * 0.40
                if quieten:
                    pixels[x, y] = mix(pixels[x, y], background[x, y], quieten)
    draw.line((0, height - 1, width - 1, height - 1), fill=mix(page, (0, 0, 0), 0.35))
    return image


def palette(accent, active, page, panel):
    white = (244, 246, 250)
    return [
        ("PRIMARY_COLOR", white),
        ("SECONDARY_BGCOLOR", mix(panel, white, 0.10)),
        ("HIGHLIGHT_COLOR", accent),
        ("HIGHLIGHT_CONTRASTING_COLOR", contrasting(accent, white)),
        ("DISABLE_COLOR", mix(panel, white, 0.34)),
        ("PRIMARY_BGCOLOR", panel),
        ("OVERLAY_COLOR", None),
        ("SECONDARY_COLOR", mix(accent, white, 0.55)),
        ("SAFE_COLOR", (72, 226, 138)),
        ("PAGE_BGCOLOR", page),
        ("ERROR_COLOR", (255, 82, 92)),
        ("ACTIVE_COLOR", active),
        ("INACTIVE_COLOR", mix(panel, white, 0.42)),
        ("BUTTON_BORDER_ACTIVE_COLOR", mix(active, white, 0.10)),
        ("BUTTON_BORDER_COLOR", mix(panel, white, 0.22)),
        ("WARNING_COLOR", (255, 199, 72)),
        ("SAFE_CONTRASTING_COLOR", (6, 22, 11)),
        ("TOPLCD_BGCOLOR", page),
    ]


def build(defn) -> None:
    slug, name, key, style, accent_hex, active_hex, page_hex, panel_hex, seed = defn
    accent, active = rgb(accent_hex), rgb(active_hex)
    page, panel = rgb(page_hex), rgb(panel_hex)

    theme_dir = THEMES_ROOT / f"theme-{slug}"
    if theme_dir.exists():
        shutil.rmtree(theme_dir)
    theme_dir.mkdir(parents=True)

    large_name, small_name = write_theme_files(
        theme_dir,
        name=name,
        key=key,
        family="Texture",
        label="Collection",
        slug=slug,
        header="Standalone ETHOS radio theme. Rotorflight and RF Suite files are not modified.",
        round_buttons=False,
        focus_style="outline",
        roles=palette(accent, active, page, panel),
        release_notes=(
            f"First stable {name} release from the Texture collection, featuring "
            f"{DESCRIPTIONS[slug]}. Custom radio-theme artwork only; no Rotorflight "
            "or RF Suite files are changed."
        ),
        readme_extra="- Does not modify Rotorflight or RF Suite Lua files\n",
    )

    for width, filename in ((X20_SIZE[0], large_name), (X18_SIZE[0], small_name)):
        save_png(toolbar(width, style, page, panel, accent, active, seed), theme_dir / filename)

    write_release(theme_dir, RELEASES_ROOT / f"{name}-v{THEME_VERSION}.zip")


def main() -> None:
    keys = [item[2] for item in THEMES]
    if len(keys) != len(set(keys)) or any(len(key) > 7 for key in keys):
        raise SystemExit("Theme keys must be unique and <=7 characters")
    for theme in THEMES:
        build(theme)
    print(f"Generated {len(THEMES)} Texture themes")


if __name__ == "__main__":
    main()
