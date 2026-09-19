"""Build the Elements collection.

Four standalone themes, each named for a natural phenomenon and each drawing
its toolbar from a different procedural technique: stacked elevation contours,
banded aurora curtains, expanding sonar rings, and a split light spectrum.

The artwork is rendered natively at both display widths rather than downscaled
from the 784px version, so the fine lines in each design stay crisp on a
480px X18 instead of blurring across the resample.
"""

from __future__ import annotations

import math
import random
import shutil

from PIL import Image, ImageDraw

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
    ("summit", "Summit", "Summit", "contour", "#E8A33D", "#FFD08A", "#0E0D0B", "#221E18", 511),
    ("aurora", "Aurora", "Aurora", "aurora", "#4BE38B", "#A66CFF", "#060A10", "#111C2C", 512),
    ("abyss", "Abyss", "Abyss", "sonar", "#2BC8FF", "#7FE9FF", "#04090E", "#0C1826", 513),
    ("prism", "Prism", "Prism", "prism", "#B06CFF", "#FFC94A", "#09080E", "#1A1626", 514),
]

SPECTRUM = ["#FF4D5E", "#FF9A3D", "#FFD24A", "#5FE08B", "#3DC9FF", "#8A6CFF"]


def wordmark_bend(x, width):
    """Ease bright geometry around the lettering without covering the artwork."""
    distance = abs(x - (width - 1) / 2)
    amount = max(0.0, min(1.0, (120 - distance) / 44))
    return amount * amount * (3 - 2 * amount)


def contour(draw, w, h, page, panel, accent, active, rng):
    """Stacked elevation lines, kept clear of the bar edges."""
    for level in range(6):
        strength = 0.22 + 0.07 * level
        points = []
        for x in range(0, w + 4, 4):
            t = x / w
            y = 10 + level * 5.2 + 2.6 * math.sin(t * 6.2 + level * 0.35) + 1.4 * math.sin(t * 15.5 + level * 0.8)
            # Upper/lower contour lines flow around the letters as a single field.
            destination = 3 + level * 3 if level < 3 else 43 + (level - 3) * 2
            bend = wordmark_bend(x, w)
            y = y * (1 - bend) + destination * bend
            points.append((x, y))
        draw.line(points, fill=mix(panel, accent, strength), width=1)

    # Concentric rings read as peaks rising out of the contour field.
    for cx, scale in ((int(w * 0.27), 1.0), (int(w * 0.71), 0.74)):
        for ring in range(4):
            rx, ry = (24 - ring * 6) * scale, (9 - ring * 2.2) * scale
            if rx <= 2 or ry <= 1:
                continue
            draw.ellipse(
                (cx - rx, 23 - ry, cx + rx, 23 + ry),
                outline=mix(panel, active, 0.30 + ring * 0.16),
            )


def aurora(draw, w, h, page, panel, accent, active, rng):
    """Vertical curtains whose hue drifts between the two theme colors."""
    for x in range(w):
        t = x / w
        wave = math.sin(t * 9.0 + 0.7) * 0.5 + math.sin(t * 21.0 + 2.1) * 0.28 + math.sin(t * 4.3) * 0.5
        top = 7 + wave * 5.5
        bottom = top + 17 + 9 * math.sin(t * 13.0 + 1.2)
        # The curtain rises over the wordmark instead of stopping at a blank gap.
        bend = wordmark_bend(x, w)
        top = top * (1 - bend) + (1 + wave * 0.5) * bend
        bottom = bottom * (1 - bend) + (9 + wave * 0.5) * bend
        hue = mix(accent, active, (math.sin(t * 12.5 + 0.4) + 1) / 2)
        # A high-frequency term breaks the band into the vertical striations
        # that make an aurora read as curtains rather than a smear.
        streak = 0.72 + 0.28 * math.sin(t * 155.0)
        intensity = (0.42 + 0.46 * (wave + 1) / 2) * streak
        span = max(bottom - top, 1)
        for y in range(max(int(top), 0), min(int(bottom), h - 5)):
            fade = 1 - (y - top) / span
            draw.point((x, y), fill=mix(page, hue, min(intensity * fade * 1.25, 0.95)))

    for _ in range(w // 26):
        x, y = rng.randrange(w), rng.randrange(0, 14)
        if abs(x - (w - 1) / 2) < 76:
            y = min(y, 9)
        draw.point((x, y), fill=mix(page, (255, 255, 255), rng.choice((0.3, 0.5, 0.75))))


def sonar(draw, w, h, page, panel, accent, active, rng):
    """Rings expanding from a source below the bar, fading with distance."""
    cx, cy = w // 2, h + 5
    for index, radius in enumerate(range(9, 132, 10)):
        brightness = max(0.06, 0.62 - radius / 165)
        points = []
        # Keep each ring continuous while its bright crest clears the lettering.
        destination = 9 if cy - radius < 27 else 43
        for degrees in range(192, 349):
            angle = math.radians(degrees)
            x = cx + radius * 2.4 * math.cos(angle)
            y = cy + radius * math.sin(angle)
            bend = wordmark_bend(x, w)
            points.append((x, y * (1 - bend) + destination * bend))
        draw.line(points, fill=mix(page, accent if index % 3 else active, brightness))
    for _ in range(w // 60):
        x = rng.randrange(w)
        y = rng.randint(8, h - 12)
        if abs(x - (w - 1) / 2) < 76:
            y = 8 if y < 25 else 43
        draw.point((x, y), fill=mix(page, active, 0.85))
    draw.line((0, h - 6, w - 1, h - 6), fill=mix(page, accent, 0.30))


def prism(draw, w, h, page, panel, accent, active, rng):
    """A single beam entering from the left and fanning into its spectrum."""
    ox, oy = int(w * 0.22), h // 2
    draw.line((0, oy - 4, ox, oy), fill=mix(page, (255, 255, 255), 0.70), width=3)

    bands = len(SPECTRUM)
    for index, value in enumerate(SPECTRUM):
        spread = (index - (bands - 1) / 2) / bands
        top, bottom, centerline = [], [], []
        # The spectrum splits around the wordmark, then resumes its original fan.
        destination = 3 + index * 3 if index < 3 else 43 + (index - 3) * 2
        for x in range(ox, w + 4, 4):
            amount = (x - ox) / (w - ox)
            y = oy + spread * h * 0.95 * amount
            bend = wordmark_bend(x, w)
            y = y * (1 - bend) + destination * bend
            thickness = (3 + amount * 2) * (1 - bend) + bend
            top.append((x, y - thickness))
            bottom.append((x, y + thickness))
            centerline.append((x, y))
        draw.polygon(top + list(reversed(bottom)), fill=mix(page, rgb(value), 0.42))
        draw.line(centerline, fill=mix(page, rgb(value), 0.85))
    draw.ellipse((ox - 3, oy - 3, ox + 3, oy + 3), fill=mix(page, (255, 255, 255), 0.8))


STYLES = {"contour": contour, "aurora": aurora, "sonar": sonar, "prism": prism}


def toolbar(width, style, page, panel, accent, active, seed) -> Image.Image:
    height = X20_SIZE[1]
    image = Image.new("RGB", (width, height), page)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        draw.line((0, y, width - 1, y), fill=mix(page, panel, (y / (height - 1)) * 0.85))
    STYLES[style](draw, width, height, page, panel, accent, active, random.Random(seed))
    draw.line((0, height - 1, width - 1, height - 1), fill=mix(page, (0, 0, 0), 0.35))
    return image


def palette(accent, active, page, panel):
    white = (244, 246, 250)
    secondary_bg = mix(panel, white, 0.10)
    return [
        ("PRIMARY_COLOR", white),
        ("SECONDARY_BGCOLOR", secondary_bg),
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


DESCRIPTIONS = {
    "summit": "stacked elevation contours with two peak rings",
    "aurora": "banded aurora curtains drifting between green and violet",
    "abyss": "sonar rings expanding from below the bar",
    "prism": "a light beam splitting into its full spectrum",
}


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
        family="Elements",
        label="Collection",
        slug=slug,
        header="Standalone ETHOS radio theme. Rotorflight and RF Suite files are not modified.",
        round_buttons=False,
        focus_style="outline",
        roles=palette(accent, active, page, panel),
        release_notes=(
            f"First stable {name} release from the Elements collection, featuring "
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
    print(f"Generated {len(THEMES)} Elements themes")


if __name__ == "__main__":
    main()
