from __future__ import annotations

import json
import math
import re
import shutil
import zipfile
from collections import defaultdict
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
THEMES_ROOT = ROOT / "themes"
RELEASES_ROOT = ROOT / "releases"
README_PATH = ROOT / "README.md"
TESTING_ROOT = ROOT / "testing"

X20_SIZE = (784, 50)
X18_SIZE = (464, 50)
EXPECTED_THEME_COUNT = 55
CLASSIC_FOLDER = "theme-rfsuite-blue"
CLASSIC_RELEASE = "RF-Suite-Blue-v1.0.5.zip"

TOOLBAR_CALL = re.compile(
    r'toolbarBackground\s*=\s*lcd\.loadBitmap\("(?P<name>[^"\n]+\.png)"\)'
)

SELECTOR = '''local function selectToolbar(largeFile, smallFile)
    local version = system.getVersion()
    if version and version.lcdWidth and version.lcdWidth <= 480 then
        return smallFile
    end
    return largeFile
end

'''


def theme_directories() -> list[Path]:
    return sorted(
        path for path in THEMES_ROOT.iterdir()
        if path.is_dir() and (path / "main.lua").exists()
    )


def find_large_toolbar(theme_dir: Path) -> Path:
    candidates = []
    for path in theme_dir.glob("toolbar*.png"):
        if path.stem.endswith("-x18"):
            continue
        try:
            with Image.open(path) as image:
                width, height = image.size
        except OSError:
            continue
        if height == 50:
            candidates.append((width, path))

    if not candidates:
        raise ValueError(f"No 50px toolbar found in {theme_dir}")

    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def x18_name(large_toolbar: Path) -> str:
    return f"{large_toolbar.stem}-x18{large_toolbar.suffix}"


def source_x_for_output(output_x: int, source_width: int) -> float:
    """Map an X18 column to the X20 artwork while preserving edges and center art.

    Wide empty/repeating areas are compressed in short transition bands. The first
    80px, centered 304px design area, and last 80px remain visually stable.
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


def make_x18_toolbar(large_toolbar: Path, small_toolbar: Path) -> None:
    # Keep the physically tested Aviation HUD asset exactly as approved.
    if small_toolbar.exists() and large_toolbar.name == "toolbar-aviation-hud.png":
        with Image.open(small_toolbar) as existing:
            if existing.size == X18_SIZE:
                return

    with Image.open(large_toolbar) as opened:
        source = opened.convert("RGB")

    if source.size == X18_SIZE:
        source.save(small_toolbar, optimize=True)
        return

    if source.height != 50:
        new_width = max(1, round(source.width * 50 / source.height))
        source = source.resize((new_width, 50), Image.Resampling.LANCZOS)

    output = Image.new("RGB", X18_SIZE)
    for output_x in range(X18_SIZE[0]):
        source_x = source_x_for_output(output_x, source.width)
        low = max(0, min(source.width - 1, math.floor(source_x)))
        high = max(0, min(source.width - 1, low + 1))
        fraction = source_x - low
        low_column = source.crop((low, 0, low + 1, 50))
        if high == low or fraction <= 0:
            column = low_column
        else:
            high_column = source.crop((high, 0, high + 1, 50))
            column = Image.blend(low_column, high_column, fraction)
        output.paste(column, (output_x, 0))

    output.save(small_toolbar, optimize=True)


def make_main_responsive(theme_dir: Path, large_name: str, small_name: str) -> None:
    path = theme_dir / "main.lua"
    text = path.read_text(encoding="utf-8")

    if "lcdWidth" in text and small_name in text:
        return

    match = TOOLBAR_CALL.search(text)
    if not match:
        raise ValueError(f"Could not locate toolbarBackground in {path}")

    referenced = match.group("name")
    if referenced != large_name:
        raise ValueError(f"{path} references {referenced}, expected {large_name}")

    init_marker = "local function init()"
    if init_marker not in text:
        raise ValueError(f"Could not locate init function in {path}")

    text = text.replace(init_marker, SELECTOR + init_marker, 1)
    text = TOOLBAR_CALL.sub(
        f'toolbarBackground = lcd.loadBitmap(selectToolbar("{large_name}", "{small_name}"))',
        text,
        count=1,
    )
    path.write_text(text, encoding="utf-8", newline="\n")


def update_theme_readme(theme_dir: Path) -> None:
    path = theme_dir / "README.md"
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")
    text = text.replace("# Aviation HUD v1.0.1-beta1", "# Aviation HUD v1.0.0")
    text = text.replace("**Status:** X18 compatibility test\n\n", "")
    text = text.replace("Static 784x50 toolbar", "Responsive 784x50 X20 / 464x50 X18 toolbar")
    text = text.replace("static 784x50 toolbar", "responsive 784x50 X20 / 464x50 X18 toolbar")
    text = text.replace("Lightweight 784x50 toolbar", "Responsive 784x50 X20 / 464x50 X18 toolbar")
    text = text.replace("lightweight 784x50 toolbar", "responsive 784x50 X20 / 464x50 X18 toolbar")

    compatibility = "- Automatically selects 784x50 artwork on 800px radios and 464x50 artwork on standard X18 radios"
    if "464x50" not in text:
        install_markers = ("\nCopy `", "\nReplace the existing `")
        inserted = False
        for marker in install_markers:
            if marker in text:
                text = text.replace(marker, f"\n{compatibility}\n{marker}", 1)
                inserted = True
                break
        if not inserted:
            text = text.rstrip() + f"\n\n{compatibility}\n"

    if theme_dir.name == CLASSIC_FOLDER:
        text = text.replace("v1.0.4", "v1.0.5")

    path.write_text(text, encoding="utf-8", newline="\n")


def update_manifest(theme_dir: Path) -> None:
    path = theme_dir / "ethos_lua_manifest.json"
    if not path.exists():
        return

    data = json.loads(path.read_text(encoding="utf-8"))
    if theme_dir.name == "theme-aviation-hud" and data.get("version") == "1.0.1-beta1":
        data["version"] = "1.0.0"
    if theme_dir.name == CLASSIC_FOLDER:
        data["version"] = "1.0.5"

    notes = data.setdefault("releaseNotes", {}).get("content", "")
    notes = notes.replace("lightweight 784x50 toolbar", "responsive X18/X20 toolbar")
    notes = notes.replace("Lightweight 784x50 toolbar", "Responsive X18/X20 toolbar")
    sentence = "Automatically selects 464x50 artwork on standard X18 radios and 784x50 artwork on 800px radios."
    if sentence not in notes:
        notes = notes.rstrip()
        if notes and not notes.endswith((".", "!", "?")):
            notes += "."
        notes = (notes + " " + sentence).strip()
    data["releaseNotes"]["content"] = notes

    path.write_text(json.dumps(data, indent=4) + "\n", encoding="utf-8", newline="\n")


def scan_release_mapping() -> dict[str, list[Path]]:
    mapping: dict[str, list[Path]] = defaultdict(list)
    for release in sorted(RELEASES_ROOT.glob("*.zip")):
        try:
            with zipfile.ZipFile(release, "r") as archive:
                roots = {
                    name.split("/", 1)[0]
                    for name in archive.namelist()
                    if "/" in name and name.split("/", 1)[0]
                }
        except zipfile.BadZipFile as error:
            raise ValueError(f"Bad existing release ZIP: {release}") from error

        theme_roots = [root for root in roots if (THEMES_ROOT / root).is_dir()]
        if len(theme_roots) == 1:
            mapping[theme_roots[0]].append(release)
    return mapping


def write_release(theme_dir: Path, release: Path) -> None:
    folder = theme_dir.name
    if release.exists():
        release.unlink()

    with zipfile.ZipFile(release, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        directory = zipfile.ZipInfo(folder + "/")
        directory.external_attr = (0o40777 << 16) | 0x10
        archive.writestr(directory, b"")
        for item in sorted(theme_dir.iterdir(), key=lambda candidate: candidate.name):
            if item.is_file() and item.name != "main.luac":
                archive.write(item, f"{folder}/{item.name}")

    with zipfile.ZipFile(release, "r") as archive:
        if archive.testzip() is not None:
            raise ValueError(f"Corrupt rebuilt release: {release}")
        names = set(archive.namelist())
        x18_assets = [name for name in names if name.endswith("-x18.png")]
        if not x18_assets:
            raise ValueError(f"Responsive asset missing from {release}")
        source = archive.read(f"{folder}/main.lua").decode("utf-8")
        if "lcdWidth" not in source:
            raise ValueError(f"Responsive selection missing from {release}")


def rebuild_releases(themes: list[Path]) -> int:
    mapping = scan_release_mapping()
    rewritten = 0

    for theme_dir in themes:
        releases = mapping.get(theme_dir.name, [])
        if theme_dir.name == CLASSIC_FOLDER:
            # Preserve the historical v1.0.3 package and add a new current release.
            releases = [path for path in releases if path.name != "RF-Suite-Blue-v1.0.3.zip"]
            current = RELEASES_ROOT / CLASSIC_RELEASE
            if current not in releases:
                releases.append(current)

        if not releases:
            raise ValueError(f"No release ZIP maps to {theme_dir.name}")

        for release in releases:
            write_release(theme_dir, release)
            rewritten += 1

    return rewritten


def update_root_readme() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    compatibility = '''## Radio compatibility

Every current theme download automatically selects the correct toolbar artwork: **784x50** on 800px radios such as the X20 Pro and X18RS, or **464x50** on standard 480px X18 radios. One ZIP works on both display sizes. Rotorflight and RF Suite Lua files are not modified.

'''
    if "## Radio compatibility" not in text:
        intro = "Custom FrSky ETHOS themes focused on improving Rotorflight RF Suite and the wider ETHOS interface.\n\n"
        if intro not in text:
            raise ValueError("README introduction changed; cannot insert compatibility section")
        text = text.replace(intro, intro + compatibility, 1)

    text = text.replace("a static 784x50 toolbar", "responsive 784x50/464x50 toolbar artwork")
    text = text.replace("a lightweight 784x50 toolbar", "responsive 784x50/464x50 toolbar artwork")
    text = text.replace("static 784x50 toolbar", "responsive 784x50/464x50 toolbar artwork")
    text = text.replace("lightweight 784x50 toolbar", "responsive 784x50/464x50 toolbar artwork")

    text = text.replace("**RF Suite Blue v1.0.4**", "**RF Suite Blue v1.0.5**")
    current_link = "- [Download current responsive release v1.0.5](releases/RF-Suite-Blue-v1.0.5.zip)\n"
    previous_link = "- [Download previous packaged release v1.0.3](releases/RF-Suite-Blue-v1.0.3.zip)"
    if current_link.strip() not in text:
        text = text.replace(previous_link, current_link + previous_link, 1)

    development_line = "- `tools/add_x18_support_all_themes.py` regenerates 464x50 X18 artwork, applies automatic display-size selection, validates all themes, and rebuilds the existing separate ZIPs.\n"
    if development_line.strip() not in text:
        marker = "## Development\n\n"
        text = text.replace(marker, marker + development_line, 1)

    README_PATH.write_text(text, encoding="utf-8", newline="\n")


def remove_beta_testing_files() -> None:
    for name in ("Aviation-HUD-X18-Test-v1.0.1-beta1.zip", "README-X18-TEST.md"):
        path = TESTING_ROOT / name
        if path.exists():
            path.unlink()
    if TESTING_ROOT.exists() and not any(TESTING_ROOT.iterdir()):
        TESTING_ROOT.rmdir()


def validate_catalog(themes: list[Path]) -> None:
    if len(themes) != EXPECTED_THEME_COUNT:
        raise ValueError(f"Expected {EXPECTED_THEME_COUNT} themes, found {len(themes)}")

    keys = set()
    for theme_dir in themes:
        large = find_large_toolbar(theme_dir)
        small = theme_dir / x18_name(large)
        with Image.open(large) as image:
            if image.size != X20_SIZE:
                raise ValueError(f"Unexpected X20 toolbar size in {large}: {image.size}")
        with Image.open(small) as image:
            if image.size != X18_SIZE:
                raise ValueError(f"Unexpected X18 toolbar size in {small}: {image.size}")

        source = (theme_dir / "main.lua").read_text(encoding="utf-8")
        if "system.getVersion()" not in source or "lcdWidth" not in source or small.name not in source:
            raise ValueError(f"Theme is not responsive: {theme_dir.name}")

        manifest_path = theme_dir / "ethos_lua_manifest.json"
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            key = manifest.get("key")
            if key in keys:
                raise ValueError(f"Duplicate manifest key: {key}")
            keys.add(key)


def main() -> None:
    themes = theme_directories()
    if len(themes) != EXPECTED_THEME_COUNT:
        raise SystemExit(f"Expected {EXPECTED_THEME_COUNT} themes before migration, found {len(themes)}")

    for theme_dir in themes:
        large = find_large_toolbar(theme_dir)
        small = theme_dir / x18_name(large)
        make_x18_toolbar(large, small)
        make_main_responsive(theme_dir, large.name, small.name)
        update_theme_readme(theme_dir)
        update_manifest(theme_dir)

    update_root_readme()
    remove_beta_testing_files()
    rewritten = rebuild_releases(themes)
    validate_catalog(themes)
    print(f"Added X18/X20 automatic toolbar support to {len(themes)} themes and rebuilt {rewritten} release ZIPs")


if __name__ == "__main__":
    main()
