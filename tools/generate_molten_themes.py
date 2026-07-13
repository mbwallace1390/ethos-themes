from __future__ import annotations

import json
import random
import shutil
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
THEMES_ROOT = ROOT / "themes"
RELEASES_ROOT = ROOT / "releases"

X20_SIZE = (784, 50)
X18_SIZE = (464, 50)

# slug, display name, short ETHOS key, focus/active hex, ember spark hex, seed
THEMES = [
    ("molten-ember", "Molten Ember", "MltEmbr", "#FF3D1A", "#FFB25C", 401),
    ("molten-sulfur", "Molten Sulfur", "MltSulf", "#CFFF3D", "#FFF4A3", 402),
    ("molten-verdigris", "Molten Verdigris", "MltVerd", "#2DEBAA", "#9CFFE0", 403),
]


def rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def mix(a: tuple[int, int, int], b: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(round(a[i] * (1 - amount) + b[i] * amount) for i in range(3))


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


def lua_color(c: tuple[int, int, int]) -> str:
    return f"lcd.RGB(0x{c[0]:02X}, 0x{c[1]:02X}, 0x{c[2]:02X})"


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

    large_name = f"toolbar-{slug}.png"
    small_name = f"toolbar-{slug}-x18.png"
    toolbar(X20_SIZE[0], p["page"], p["primary_bg"], focus, active, seed).save(theme_dir / large_name, optimize=True)
    toolbar(X18_SIZE[0], p["page"], p["primary_bg"], focus, active, seed).save(theme_dir / small_name, optimize=True)

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
    color_lines = [f"            {'COLOR_BLACK' if value is None else lua_color(value)}, -- {role}" for role, value in roles]
    lua = f'''-- {name}
-- Lightweight standalone ETHOS theme.
local function selectToolbar(largeFile, smallFile)
    local version = system.getVersion()
    if version and version.lcdWidth and version.lcdWidth <= 480 then
        return smallFile
    end
    return largeFile
end

local function init()
    system.registerTheme({{
        key = "{key}",
        name = "{name}",
        roundButtons = {str(p["round"]).lower()},
        focusStyle = "{p["focus_style"]}",
        colors = {{
{chr(10).join(color_lines)}
        }},
        toolbarBackground = lcd.loadBitmap(selectToolbar("{large_name}", "{small_name}")),
    }})
end

return {{ init = init }}
'''
    (theme_dir / "main.lua").write_text(lua, encoding="utf-8", newline="\n")

    manifest = {
        "manifestVersion": 1,
        "name": name,
        "key": f"mbwallace1390-theme-{key}",
        "version": "1.0.0",
        "releaseNotes": {
            "format": "markdown",
            "content": (
                f"First stable {name} release from the Molten family. Automatically selects 464x50 "
                "artwork on standard X18 radios and 784x50 artwork on 800px radios."
            ),
        },
        "folder": folder,
        "files": ["main.lua", "toolbar-*"],
    }
    (theme_dir / "ethos_lua_manifest.json").write_text(json.dumps(manifest, indent=4) + "\n", encoding="utf-8", newline="\n")
    (theme_dir / "README.md").write_text(
        f"# {name} v1.0.0\n\n**Family:** Molten\n\nA lightweight standalone FrSky ETHOS theme.\n\n"
        f"- Focus: `{p['focus_style']}`\n- Controls: {'rounded' if p['round'] else 'square'}\n- Internal key: `{key}`\n"
        f"- Automatically selects 784x50 artwork on 800px radios and 464x50 artwork on standard X18 radios\n\n"
        f"Copy `{folder}` into the transmitter `scripts` folder, restart, and select **{name}**.\n",
        encoding="utf-8",
        newline="\n",
    )

    release = RELEASES_ROOT / f"{'-'.join(word.capitalize() for word in slug.split('-'))}-v1.0.0.zip"
    if release.exists():
        release.unlink()
    with zipfile.ZipFile(release, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        info = zipfile.ZipInfo(folder + "/")
        info.external_attr = (0o40777 << 16) | 0x10
        archive.writestr(info, b"")
        for item in sorted(theme_dir.iterdir(), key=lambda x: x.name):
            archive.write(item, f"{folder}/{item.name}")

    with zipfile.ZipFile(release, "r") as archive:
        if archive.testzip() is not None:
            raise ValueError(f"Corrupt ZIP: {release}")
        if f"{folder}/main.luac" in archive.namelist():
            raise ValueError("main.luac must not be packaged")
        with archive.open(f"{folder}/{large_name}") as fh:
            if Image.open(fh).size != X20_SIZE:
                raise ValueError("Wrong X20 toolbar size")
        with archive.open(f"{folder}/{small_name}") as fh:
            if Image.open(fh).size != X18_SIZE:
                raise ValueError("Wrong X18 toolbar size")


if __name__ == "__main__":
    keys = [item[2] for item in THEMES]
    if len(keys) != len(set(keys)) or any(len(key) > 7 for key in keys):
        raise SystemExit("Theme keys must be unique and <=7 characters")
    for theme in THEMES:
        build(theme)
    print(f"Generated {len(THEMES)} Molten themes")
