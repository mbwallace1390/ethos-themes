from __future__ import annotations

import zipfile
from pathlib import Path
from PIL import Image, ImageDraw

from generate_custom_art_themes import THEMES, artwork, color, mix

ROOT = Path(__file__).resolve().parents[1]
THEME_DIR = ROOT / "themes" / "theme-aviation-hud"
TESTING_DIR = ROOT / "testing"
X18_TOOLBAR = THEME_DIR / "toolbar-aviation-hud-x18.png"
X20_TOOLBAR = THEME_DIR / "toolbar-aviation-hud.png"
TEST_ZIP = TESTING_DIR / "Aviation-HUD-X18-Test-v1.0.1-beta1.zip"


def make_x18_toolbar() -> None:
    theme = next(item for item in THEMES if item[1] == "aviation-hud")
    _, _, _, _, _, style, _, _, palette = theme
    page = color(palette[8])
    panel = color(palette[5])
    accent = color(palette[2])
    active = color(palette[10])

    width, height = 464, 50
    image = Image.new("RGB", (width, height), page)
    draw = ImageDraw.Draw(image)
    artwork(draw, style, width, height, page, panel, accent, active)
    draw.line((0, height - 1, width - 1, height - 1), fill=mix(page, (0, 0, 0), 0.35))
    image.save(X18_TOOLBAR, optimize=True)


def validate_sources() -> None:
    with Image.open(X20_TOOLBAR) as image:
        if image.size != (784, 50):
            raise ValueError(f"Unexpected X20 toolbar size: {image.size}")
    with Image.open(X18_TOOLBAR) as image:
        if image.size != (464, 50):
            raise ValueError(f"Unexpected X18 toolbar size: {image.size}")

    source = (THEME_DIR / "main.lua").read_text(encoding="utf-8")
    required = ["system.getVersion()", "lcdWidth", "toolbar-aviation-hud-x18.png", "toolbar-aviation-hud.png"]
    for text in required:
        if text not in source:
            raise ValueError(f"Missing responsive-theme marker: {text}")


def build_test_zip() -> None:
    TESTING_DIR.mkdir(parents=True, exist_ok=True)
    if TEST_ZIP.exists():
        TEST_ZIP.unlink()

    folder = THEME_DIR.name
    with zipfile.ZipFile(TEST_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        directory = zipfile.ZipInfo(folder + "/")
        directory.external_attr = (0o40777 << 16) | 0x10
        archive.writestr(directory, b"")
        for item in sorted(THEME_DIR.iterdir(), key=lambda path: path.name):
            if item.name == "main.luac":
                continue
            archive.write(item, f"{folder}/{item.name}")

    with zipfile.ZipFile(TEST_ZIP, "r") as archive:
        if archive.testzip() is not None:
            raise ValueError("Test ZIP is corrupt")
        names = set(archive.namelist())
        required = {
            f"{folder}/main.lua",
            f"{folder}/ethos_lua_manifest.json",
            f"{folder}/toolbar-aviation-hud.png",
            f"{folder}/toolbar-aviation-hud-x18.png",
        }
        if not required.issubset(names):
            raise ValueError(f"Test ZIP missing files: {sorted(required - names)}")


def main() -> None:
    make_x18_toolbar()
    validate_sources()
    build_test_zip()
    print(f"Generated {X18_TOOLBAR.relative_to(ROOT)} and {TEST_ZIP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
