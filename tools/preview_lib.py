"""Shared, source-driven catalog previews; never installed on a radio."""
from __future__ import annotations

import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
THEMES_ROOT = ROOT / "themes"
PREVIEWS_ROOT = ROOT / "previews"
ROLE_RE = re.compile(r"lcd\.RGB\(0x([0-9A-Fa-f]{2}),\s*0x([0-9A-Fa-f]{2}),\s*0x([0-9A-Fa-f]{2})\),\s*--\s*([A-Z_]+)")


def font(size, bold=False):
    paths = (
        "C:/Windows/Fonts/seguisb.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    )
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    # Preview labels intentionally use ASCII so this fallback has every glyph.
    return ImageFont.load_default(size=size)


def parse_theme(slug):
    folder = THEMES_ROOT / f"theme-{slug}"
    source = (folder / "main.lua").read_text(encoding="utf-8")
    colors = {role: (int(r, 16), int(g, 16), int(b, 16))
              for r, g, b, role in ROLE_RE.findall(source)}
    name = re.search(r'name\s*=\s*"([^"]+)"', source)
    rounded = re.search(r"roundButtons\s*=\s*(true|false)", source)
    focus = re.search(r'focusStyle\s*=\s*"([^"]+)"', source)
    art = [p for p in folder.glob("toolbar-*.png") if not p.stem.endswith("-x18")]
    logo = re.search(r'pcall\(lcd\.loadBitmap,\s*"(logo-[^"]+\.png)"\)', source)
    if not name or not rounded or not focus or len(colors) != 17 or len(art) != 1:
        raise ValueError(f"Incomplete native theme: {folder}")
    return {"name": name[1], "round": rounded[1] == "true", "focus": focus[1],
            "colors": colors, "toolbar": art[0],
            "logo": folder / logo[1] if logo else None}


def toolbar_preview(theme):
    """Composite shipped assets at the representative centered logo position.

    ETHOS owns the final layout. This is a catalog illustration, not a capture
    of the firmware screen. Baked-header themes use an invisible 1x1 override.
    """
    with Image.open(theme["toolbar"]) as art:
        strip = art.convert("RGB")
    if theme.get("logo"):
        with Image.open(theme["logo"]) as source:
            logo = source.convert("RGBA")
            strip.paste(logo, ((strip.width - logo.width) // 2,
                              (strip.height - logo.height) // 2), logo)
    return strip


def centered(draw, bounds, label, face, color):
    left, top, right, bottom = bounds
    box = draw.textbbox((0, 0), label, font=face)
    draw.text(((left + right - box[2] + box[0]) / 2,
               (top + bottom - box[3] + box[1]) / 2 - box[1]),
              label, font=face, fill=color)


def draw_card(canvas, theme, x, y):
    draw = ImageDraw.Draw(canvas)
    c = theme["colors"]
    width, height = 552, 366
    page, panel, border = c["PAGE_BGCOLOR"], c["PRIMARY_BGCOLOR"], c["BUTTON_BORDER_COLOR"]
    accent, text = c["HIGHLIGHT_COLOR"], c["PRIMARY_COLOR"]
    draw.rounded_rectangle((x, y, x + width, y + height), radius=13,
                           fill=page, outline=border, width=2)
    draw.rectangle((x + 18, y + 20, x + 22, y + 50), fill=accent)
    title = font(23, True)
    while draw.textlength(theme["name"], font=title) > 382:
        title = font(title.size - 1, True)
    draw.text((x + 34, y + 15), theme["name"], font=title, fill=text)
    draw.text((x + 431, y + 24), theme["focus"].upper(), font=font(12, True), fill=c["SECONDARY_COLOR"])

    # This is explicitly a scaled catalog sample; native art ships unchanged.
    strip = toolbar_preview(theme).resize((512, 33), Image.Resampling.LANCZOS)
    canvas.paste(strip, (x + 20, y + 65))
    radius = 8 if theme["round"] else 0
    for index, label in enumerate(("Selected", "Normal", "Active", "Disabled")):
        bx, by = x + 20 + index % 2 * 266, y + 119 + index // 2 * 87
        fill, edge, foreground = panel, border, text
        if index == 0:
            edge = accent
            if theme["focus"] == "invert":
                fill, foreground = accent, c["HIGHLIGHT_CONTRASTING_COLOR"]
        elif index == 2:
            edge, foreground = c["BUTTON_BORDER_ACTIVE_COLOR"], c["ACTIVE_COLOR"]
        elif index == 3:
            foreground = c["DISABLE_COLOR"]
        bounds = (bx, by, bx + 246, by + 67)
        draw.rounded_rectangle(bounds, radius=radius, fill=fill, outline=edge,
                               width=3 if index == 0 else 1)
        centered(draw, bounds, label, font(19, index == 0), foreground)
    # Show selected-fill text as well as outline focus: ETHOS uses highlight
    # colors in more places than the simple focus boxes shown above.
    draw.rounded_rectangle((x + 20, y + 291, x + 179, y + 325), radius=5, fill=accent)
    centered(draw, (x + 20, y + 291, x + 179, y + 325), "Highlight text", font(14, True), c["HIGHLIGHT_CONTRASTING_COLOR"])
    draw.rounded_rectangle((x + 191, y + 291, x + 333, y + 325), radius=5, fill=c["SAFE_COLOR"])
    centered(draw, (x + 191, y + 291, x + 333, y + 325), "Safe", font(14, True), c["SAFE_CONTRASTING_COLOR"])
    draw.text((x + 352, y + 298), "Inactive", font=font(14), fill=c["INACTIVE_COLOR"])
    draw.text((x + 20, y + 340), "ROUNDED CONTROLS" if theme["round"] else "SQUARE CONTROLS",
              font=font(10), fill=c["SECONDARY_COLOR"])
    for index, role in enumerate(("HIGHLIGHT_COLOR", "ACTIVE_COLOR", "WARNING_COLOR", "ERROR_COLOR")):
        left = x + 450 + index * 22
        draw.ellipse((left, y + 341, left + 12, y + 353), fill=c[role])


def render_collection(slug, title, theme_slugs, *, display_names=None):
    themes = [parse_theme(name) for name in theme_slugs]
    # Catalog labels can differ from legacy package names without renaming installs.
    for theme_slug, theme in zip(theme_slugs, themes):
        if display_names and theme_slug in display_names:
            theme["name"] = display_names[theme_slug]
    rows = (len(themes) + 1) // 2
    height = 160 + rows * 394
    canvas = Image.new("RGB", (1200, height), (7, 12, 21))
    draw = ImageDraw.Draw(canvas)
    draw.text((36, 25), "ETHOS 26  /  THE THEME COLLECTION", font=font(13, True), fill=(140, 169, 198))
    draw.text((33, 46), title, font=font(36, True), fill=(245, 247, 250))
    draw.text((36, 101), f"{len(themes):02d} THEMES  |  Actual palettes and artwork  |  Illustrative layout",
              font=font(15), fill=(168, 185, 203))
    for index, theme in enumerate(themes):
        draw_card(canvas, theme, 36 + index % 2 * 576, 144 + index // 2 * 394)
    PREVIEWS_ROOT.mkdir(parents=True, exist_ok=True)
    canvas.save(PREVIEWS_ROOT / f"{slug}.png", optimize=True)
