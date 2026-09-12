"""Shared helpers for the ETHOS theme generators.

Every generator writes the same three things: palette-encoded toolbar art at
both display sizes, a ``main.lua`` that picks the right art at runtime, and a
release ZIP. Keeping that in one place stops a regeneration from silently
undoing the X18 responsive support or the palette encoding.
"""

from __future__ import annotations

import json
import math
import zipfile
from pathlib import Path

from PIL import Image

from png_optimize import optimize_png
from palette_quality import polish_lua_source

ROOT = Path(__file__).resolve().parents[1]
THEMES_ROOT = ROOT / "themes"
RELEASES_ROOT = ROOT / "releases"
PREVIEWS_ROOT = ROOT / "previews"
THEME_VERSION = "1.2.0"
ETHOS26_SUPPORT = (
    "Requires ETHOS 26.1.0 or newer; API checked against 26.1.2. "
    "Radio validation is still required."
)
ETHOS26_RELEASE_NOTES = (
    "Readability update: improved foreground contrast and refreshed catalog previews. "
    "ETHOS 26.1 compatibility update, checked against the 26.1.2 theme API. "
    "Suite local ZIP layout corrected with the manifest and files at archive root. "
    "Unsupported firmware skips registration; optional toolbar load failures "
    "during initialization fall back to the theme colors. "
    "Requires ETHOS 26.1.0 or newer. Radio validation is still required."
)

X20_SIZE = (784, 50)
X18_SIZE = (464, 50)

# Radios at or below 480px load the small artwork; everything else the large.
SELECTOR_LUA = """local function selectToolbar(largeFile, smallFile)
    local version = system.getVersion()
    if version and type(version.lcdWidth) == "number" and version.lcdWidth <= 480 then
        return smallFile
    end
    return largeFile
end

local function loadToolbar(largeFile, smallFile)
    -- Optional artwork must not prevent registration when it cannot be loaded.
    local ok, bitmap = pcall(lcd.loadBitmap, selectToolbar(largeFile, smallFile))
    if ok and bitmap then
        return bitmap
    end
    return nil
end

"""

INIT_GUARD_LUA = """    -- Skip unsupported firmware before creating colors or loading artwork.
    if type(system.registerTheme) ~= "function" then return end
"""


def rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def mix(a: tuple[int, int, int], b: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(round(a[i] * (1 - amount) + b[i] * amount) for i in range(3))


def lua_color(color: tuple[int, int, int]) -> str:
    return f"lcd.RGB(0x{color[0]:02X}, 0x{color[1]:02X}, 0x{color[2]:02X})"


def contrasting(
    color: tuple[int, int, int],
    light: tuple[int, int, int] = (244, 246, 250),
    dark: tuple[int, int, int] = (12, 12, 16),
) -> tuple[int, int, int]:
    """Choose the family's initial light/dark text preference.

    This legacy luminance heuristic preserves the family design inputs. The
    final Lua writer uses polish_lua_source to enforce the actual sRGB contrast
    targets, adjusting this suggestion only if it is below the chosen target.
    """
    luminance = 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]
    return dark if luminance > 135 else light


def toolbar_call(large_name: str, small_name: str) -> str:
    return f'loadToolbar("{large_name}", "{small_name}")'


def zip_install_instructions(folder: str) -> str:
    return (
        "Install the ZIP with ETHOS Suite's local ZIP installer. For manual ZIP "
        f"installation, create `scripts/{folder}/` on the transmitter and extract "
        "the ZIP contents into that folder."
    )


def save_png(image: Image.Image, path: Path) -> None:
    """Save toolbar art as an indexed PNG, roughly a third smaller than RGB.

    Most designs use well under 256 colors, so the palette is exact and the
    round-trip is verified before being written. Smooth gradient art can exceed
    256; those are quantized with an adaptive palette, which halves the file
    again for an error far below what a 50px toolbar strip can show.
    """
    source = image.convert("RGB")
    if source.getcolors(256) is not None:
        indexed = source.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
        if indexed.convert("RGB").tobytes() == source.tobytes():
            indexed.save(path, optimize=True)
            optimize_png(path)
            return
    source.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(
        path, optimize=True
    )
    optimize_png(path)


def _source_x_for_output(output_x: int, source_width: int) -> float:
    """Map an X18 column onto the X20 artwork, preserving edges and center art.

    Wide repeating areas are compressed in short transition bands so the first
    80px, the centered 304px design area, and the last 80px stay stable.
    """
    output_anchors = (0, 80, 96, 216, 248, 368, 384, 463)
    source_anchors_784 = (0, 80, 240, 360, 424, 544, 704, 783)
    scale = (source_width - 1) / 783
    source_anchors = tuple(value * scale for value in source_anchors_784)

    for index in range(len(output_anchors) - 1):
        out_a, out_b = output_anchors[index], output_anchors[index + 1]
        if output_x <= out_b:
            src_a, src_b = source_anchors[index], source_anchors[index + 1]
            amount = (output_x - out_a) / max(out_b - out_a, 1)
            return src_a + (src_b - src_a) * amount
    return float(source_width - 1)


def downscale_to_x18(source: Image.Image) -> Image.Image:
    """Produce the 464x50 variant of a 784x50 toolbar."""
    source = source.convert("RGB")
    if source.size == X18_SIZE:
        return source
    if source.height != X20_SIZE[1]:
        width = max(1, round(source.width * X20_SIZE[1] / source.height))
        source = source.resize((width, X20_SIZE[1]), Image.Resampling.LANCZOS)

    # Resolve every column mapping first, then blend whole columns at once.
    output = Image.new("RGB", X18_SIZE)
    for output_x in range(X18_SIZE[0]):
        source_x = _source_x_for_output(output_x, source.width)
        low = max(0, min(source.width - 1, math.floor(source_x)))
        high = max(0, min(source.width - 1, low + 1))
        fraction = source_x - low
        low_column = source.crop((low, 0, low + 1, X20_SIZE[1]))
        if high == low or fraction <= 0:
            column = low_column
        else:
            column = Image.blend(low_column, source.crop((high, 0, high + 1, X20_SIZE[1])), fraction)
        output.paste(column, (output_x, 0))
    return output


def write_theme_files(
    theme_dir: Path,
    *,
    name: str,
    key: str,
    family: str,
    slug: str,
    header: str,
    round_buttons: bool,
    focus_style: str,
    roles: list[tuple[str, tuple[int, int, int] | None]],
    release_notes: str,
    label: str = "Family",
    readme_extra: str = "",
) -> tuple[str, str]:
    """Write main.lua, the manifest and the per-theme README. Returns art names."""
    large_name = f"toolbar-{slug}.png"
    small_name = f"toolbar-{slug}-x18.png"

    color_lines = [
        f"            {'COLOR_BLACK' if value is None else lua_color(value)}, -- {role}"
        for role, value in roles
    ]
    lua = f"""-- {name}
-- {header}
{SELECTOR_LUA}local function init()
{INIT_GUARD_LUA}    system.registerTheme({{
        key = "{key}",
        name = "{name}",
        roundButtons = {str(round_buttons).lower()},
        focusStyle = "{focus_style}",
        colors = {{
{chr(10).join(color_lines)}
        }},
        toolbarBackground = {toolbar_call(large_name, small_name)},
    }})
end

return {{ init = init }}
"""
    (theme_dir / "main.lua").write_text(polish_lua_source(lua), encoding="utf-8", newline="\n")

    compatibility = (
        "Automatically selects 464x50 artwork on standard X18 radios "
        "and 784x50 artwork on 800px radios."
    )
    notes = release_notes.rstrip()
    if notes and not notes.endswith((".", "!", "?")):
        notes += "."
    manifest = {
        "manifestVersion": 1,
        "name": name,
        "key": f"mbwallace1390-theme-{key}",
        "version": THEME_VERSION,
        "releaseNotes": {"format": "markdown", "content": f"{ETHOS26_RELEASE_NOTES} {notes} {compatibility}".strip()},
        "folder": theme_dir.name,
        "files": ["main.lua", "toolbar-*"],
    }
    (theme_dir / "ethos_lua_manifest.json").write_text(
        json.dumps(manifest, indent=4) + "\n", encoding="utf-8", newline="\n"
    )

    (theme_dir / "README.md").write_text(
        f"# {name} v{THEME_VERSION}\n\n{ETHOS26_SUPPORT}\n\n"
        f"{zip_install_instructions(theme_dir.name)}\n\n**{label}:** {family}\n\n"
        "A standalone FrSky ETHOS theme.\n\n"
        f"- Focus: `{focus_style}`\n"
        f"- Controls: {'rounded' if round_buttons else 'square'}\n"
        f"- Internal key: `{key}`\n"
        f"- Automatically selects 784x50 artwork on 800px radios and 464x50 artwork on standard X18 radios\n"
        f"{readme_extra}"
        f"\nTo install from repository sources, copy `{theme_dir.name}` into the transmitter `scripts` folder, restart, "
        f"and select **{name}** under **System > General > Theme**.\n",
        encoding="utf-8",
        newline="\n",
    )
    return large_name, small_name


# Fixed entry timestamp so rebuilding a release byte-for-byte reproduces it and
# regeneration does not churn git with mtime-only differences.
RELEASE_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def write_release(theme_dir: Path, release: Path) -> None:
    """Build a Suite-compatible ZIP with its manifest and files at the root.

    Suite reads ``folder`` from the root manifest to choose the radio install
    directory; it does not strip a wrapper folder from the ZIP.
    """
    manifest = json.loads((theme_dir / "ethos_lua_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("folder") != theme_dir.name:
        raise ValueError(f"Manifest folder does not match {theme_dir}")
    RELEASES_ROOT.mkdir(parents=True, exist_ok=True)
    if release.exists():
        release.unlink()

    with zipfile.ZipFile(release, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for item in sorted(theme_dir.iterdir(), key=lambda candidate: candidate.name):
            if item.is_file() and item.name != "main.luac":
                info = zipfile.ZipInfo(item.name, RELEASE_TIMESTAMP)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o100644 << 16)
                archive.writestr(info, item.read_bytes())

    with zipfile.ZipFile(release, "r") as archive:
        if archive.testzip() is not None:
            raise ValueError(f"Corrupt release ZIP: {release}")
        names = set(archive.namelist())
        if "main.luac" in names:
            raise ValueError(f"main.luac must not be packaged: {release}")
        if "ethos_lua_manifest.json" not in names:
            raise ValueError(f"Suite requires a root manifest: {release}")
        source = archive.read("main.lua").decode("utf-8")
        if "lcdWidth" not in source:
            raise ValueError(f"Responsive toolbar selection missing from {release}")
        for expected, size in (("-x18.png", X18_SIZE), (".png", X20_SIZE)):
            matches = [
                item for item in names
                if item.endswith(expected) and (expected == "-x18.png" or not item.endswith("-x18.png"))
            ]
            if not matches:
                raise ValueError(f"Missing {size[0]}x{size[1]} artwork in {release}")
            with archive.open(matches[0]) as handle:
                if Image.open(handle).size != size:
                    raise ValueError(f"Wrong artwork size for {matches[0]} in {release}")
