from __future__ import annotations

import random
import shutil
from pathlib import Path
from PIL import Image, ImageDraw

from theme_lib import (
    RELEASES_ROOT,
    THEMES_ROOT,
    X18_SIZE,
    X20_SIZE,
    mix,
    rgb,
    save_png,
    write_release,
    write_theme_files,
)

# slug, display name, short ETHOS key, focus/active hex, ember spark hex, seed
THEMES = [
    ("molten-ember", "Molten Ember", "MltEmbr", "#FF3D1A", "#FFB25C", 401),
    ("molten-sulfur", "Molten Sulfur", "MltSulf", "#CFFF3D", "#FFF4A3", 402),
    ("molten-verdigris", "Molten Verdigris", "MltVerd", "#2DEBAA", "#9CFFE0", 403),
]


def palette(focus: tuple[int, int, int], active: tuple[int, int, int]) -> dict[str, object]:
    white = (245, 241, 236)
    page = (10, 8, 7)
    primary_bg = (21, 17, 15)
    secondary_bg = (33, 27, 23)
    return dict(
        round=False, focus_style="outline", primary=white, secondary_bg=secondary_bg,
        highlight=focus, highlight_contrast=(16, 12, 10), disabled=mix(primary_bg, white, .35),
        primary_bg=primary_bg, secondary=mix(focus, white, .55), safe=(63, 235, 127), page=page,
        error=(255, 68, 77), active=active, inactive=mix(primary_bg, white, .42),
        active_border=mix(active, white, .12), border=mix(primary_bg, white, .22),
        warning=(255, 199, 56), safe_contrast=(5, 22, 10),
    )


def toolbar(width: int, page: tuple[int, int, int], primary_bg: tuple[int, int, int],
            focus: tuple[int, int, int], active: tuple[int, int, int], seed: int) -> Image.Image:
    h = 50
    image = Image.new("RGB", (width, h))
    draw = ImageDraw.Draw(image)
    for y in range(h):
        draw.line((0, y, width - 1, y), fill=mix(page, primary_bg, y / (h - 1)))

    rng = random.Random(seed)
    points = []
    y = 25
    for x in range(0, width, 14):
        y = max(17, min(34, y + rng.randint(-4, 4)))
        points.append((x, y))
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=mix(primary_bg, focus, .28), width=5)
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=focus, width=2)

    for _ in range(width // 22):
        x, yy = rng.randint(0, width - 1), rng.randint(0, h - 1)
        brightness = rng.choice((.35, .55, .75, .95))
        draw.point((x, yy), fill=mix(page, active, brightness))

    draw.line((0, h - 1, width - 1, h - 1), fill=mix(page, (0, 0, 0), .35))
    return image


def build(defn: tuple[str, str, str, str, str, int]) -> None:
    slug, name, key, focus_hex, active_hex, seed = defn
    focus, active = rgb(focus_hex), rgb(active_hex)
    p = palette(focus, active)
    folder = f"theme-{slug}"
    theme_dir = THEMES_ROOT / folder
    if theme_dir.exists():
        shutil.rmtree(theme_dir)
    theme_dir.mkdir(parents=True)
    RELEASES_ROOT.mkdir(parents=True, exist_ok=True)

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
    large_name, small_name = write_theme_files(
        theme_dir,
        name=name, key=key, family="Molten", slug=slug,
        header="Lightweight standalone ETHOS theme.",
        round_buttons=p["round"], focus_style=p["focus_style"], roles=roles,
        release_notes=f"First stable {name} release from the Molten family.",
    )
    # Procedural art is rendered natively at each width rather than downscaled,
    # which keeps the fissure a crisp single-pixel line on both displays.
    save_png(toolbar(X20_SIZE[0], p["page"], p["primary_bg"], focus, active, seed), theme_dir / large_name)
    save_png(toolbar(X18_SIZE[0], p["page"], p["primary_bg"], focus, active, seed), theme_dir / small_name)

    release = RELEASES_ROOT / f"{'-'.join(word.capitalize() for word in slug.split('-'))}-v1.0.0.zip"
    write_release(theme_dir, release)


if __name__ == "__main__":
    keys = [item[2] for item in THEMES]
    if len(keys) != len(set(keys)) or any(len(key) > 7 for key in keys):
        raise SystemExit("Theme keys must be unique and <=7 characters")
    for theme in THEMES:
        build(theme)
    print(f"Generated {len(THEMES)} Molten themes")
