"""Check every invariant the theme catalog is supposed to hold.

Safe to run at any time â€” it only reads. Run it after regenerating themes to
confirm nothing drifted: artwork sizes and encoding, responsive toolbar
selection, unique ETHOS keys, and release ZIPs that actually match the theme
folders they ship.
"""

from __future__ import annotations

from fnmatch import fnmatchcase
import json
import re
import sys
import zipfile
from pathlib import Path

from PIL import Image

from theme_lib import RELEASES_ROOT, ROOT, THEMES_ROOT, X18_SIZE, X20_SIZE

KEY_RE = re.compile(r'key\s*=\s*"([^"]+)"')
NAME_RE = re.compile(r'name\s*=\s*"([^"]+)"')
MAX_KEY_LENGTH = 7


def theme_dirs() -> list[Path]:
    return sorted(p for p in THEMES_ROOT.iterdir() if p.is_dir() and (p / "main.lua").exists())


def check_theme(theme_dir: Path, problems: list[str]) -> tuple[str | None, str | None]:
    def fail(message: str) -> None:
        problems.append(f"{theme_dir.name}: {message}")

    for required in ("main.lua", "ethos_lua_manifest.json", "README.md"):
        if not (theme_dir / required).exists():
            fail(f"missing {required}")

    source = (theme_dir / "main.lua").read_text(encoding="utf-8")
    if "main.luac" in [p.name for p in theme_dir.iterdir()]:
        fail("main.luac must not be committed")

    key_match = KEY_RE.search(source)
    name_match = NAME_RE.search(source)
    key = key_match.group(1) if key_match else None
    if key is None:
        fail("no theme key in main.lua")
    elif len(key) > MAX_KEY_LENGTH:
        fail(f"key {key!r} exceeds {MAX_KEY_LENGTH} characters")

    large = [
        p for p in theme_dir.glob("toolbar-*.png") if not p.stem.endswith("-x18")
    ]
    small = list(theme_dir.glob("toolbar-*-x18.png"))
    if len(large) != 1 or len(small) != 1:
        fail(f"expected one large and one x18 toolbar, found {len(large)}/{len(small)}")
        return key, None

    for path, expected in ((large[0], X20_SIZE), (small[0], X18_SIZE)):
        with Image.open(path) as image:
            if image.size != expected:
                fail(f"{path.name} is {image.size}, expected {expected}")
            if image.mode != "P":
                fail(f"{path.name} is {image.mode}, expected palette-encoded 'P'")

    if "system.getVersion()" not in source or "lcdWidth" not in source:
        fail("main.lua does not select artwork by display width")
    for asset in (large[0].name, small[0].name):
        if asset not in source:
            fail(f"main.lua never references {asset}")
    # Optional bitmap overrides must be present and installed just like the toolbar.
    referenced_images = set(re.findall(r'"([^"\n]+\.png)"', source))
    for asset in referenced_images:
        if not (theme_dir / asset).is_file():
            fail(f"main.lua references missing image {asset}")

    manifest_key = None
    manifest_path = theme_dir / "ethos_lua_manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            fail(f"unreadable manifest: {error}")
        else:
            manifest_key = manifest.get("key")
            if manifest.get("folder") != theme_dir.name:
                fail(f"manifest folder {manifest.get('folder')!r} does not match directory")
            if name_match and manifest.get("name") != name_match.group(1):
                fail("manifest name does not match main.lua name")
            files = manifest.get("files")
            if (not isinstance(files, list) or not files
                    or any(not isinstance(pattern, str) or not pattern for pattern in files)):
                fail("manifest files must be a nonempty list of file patterns")
            else:
                for asset in sorted({"main.lua", large[0].name, small[0].name} | referenced_images):
                    if not any(fnmatchcase(asset, pattern) for pattern in files):
                        fail(f"manifest files does not install {asset}")
                if any(fnmatchcase("main.luac", pattern) for pattern in files):
                    fail("manifest files must not install main.luac")
    return key, manifest_key


VERSION_RE = re.compile(r"-v(\d+\.\d+\.\d+)\.zip$")


def current_version(theme_dir: Path) -> str | None:
    manifest = theme_dir / "ethos_lua_manifest.json"
    if not manifest.exists():
        return None
    try:
        return json.loads(manifest.read_text(encoding="utf-8")).get("version")
    except json.JSONDecodeError:
        return None


def check_releases(problems: list[str]) -> None:
    """Every theme needs a current release whose contents match the theme folder.

    Superseded archives (a v1.0.3 ZIP kept beside the current v1.0.5) are
    deliberate snapshots of older artwork, so only the release matching the
    manifest version is compared against the working files.
    """
    packaged: set[str] = set()
    themes = {theme_dir.name: theme_dir for theme_dir in theme_dirs()}
    for release in sorted(RELEASES_ROOT.glob("*.zip")):
        try:
            with zipfile.ZipFile(release) as archive:
                if archive.testzip() is not None:
                    problems.append(f"{release.name}: corrupt archive")
                    continue
                names = archive.namelist()
                root_manifest = "ethos_lua_manifest.json" in names
                if root_manifest:
                    try:
                        manifest = json.loads(archive.read("ethos_lua_manifest.json"))
                    except (json.JSONDecodeError, UnicodeDecodeError) as error:
                        problems.append(f"{release.name}: unreadable root manifest: {error}")
                        continue
                    folder = manifest.get("folder") if isinstance(manifest, dict) else None
                    if not isinstance(folder, str) or folder not in themes:
                        problems.append(f"{release.name}: root manifest folder {folder!r} is not a catalog theme")
                        continue
                else:
                    # Only use legacy nesting to identify frozen older releases.
                    roots = {n.split("/", 1)[0] for n in names if "/" in n}
                    folders = [root for root in roots if root in themes]
                    if len(folders) != 1:
                        problems.append(f"{release.name}: missing ethos_lua_manifest.json at ZIP root")
                        continue
                    folder = folders[0]
                version_match = VERSION_RE.search(release.name)
                expected_version = current_version(THEMES_ROOT / folder)
                if version_match and expected_version and version_match.group(1) != expected_version:
                    continue  # superseded archive, intentionally frozen
                if not version_match or not expected_version:
                    problems.append(f"{release.name}: cannot establish the current manifest version")
                    continue
                if not root_manifest:
                    problems.append(f"{release.name}: missing ethos_lua_manifest.json at ZIP root; nested theme folders cannot be installed by ETHOS Suite")
                    continue
                packaged.add(folder)

                # Compare both directions: a readable ZIP can still omit its Lua,
                # manifest or one toolbar, leaving an incomplete install.
                expected_files = {
                    path.name
                    for path in (THEMES_ROOT / folder).iterdir()
                    if path.is_file() and path.name != "main.luac"
                }
                file_names = [name for name in names if not name.endswith("/")]
                actual_files = set(file_names)
                if len(file_names) != len(actual_files):
                    problems.append(f"{release.name}: duplicate file members")
                for name in sorted(expected_files - actual_files):
                    problems.append(f"{release.name}: missing {name}")
                for name in sorted(actual_files - expected_files):
                    problems.append(f"{release.name}: unexpected file {name}")
                for name in sorted(expected_files & actual_files):
                    on_disk = THEMES_ROOT / folder / name
                    if archive.read(name) != on_disk.read_bytes():
                        problems.append(f"{release.name}: {name} is stale relative to the theme folder")
        except zipfile.BadZipFile:
            problems.append(f"{release.name}: not a valid ZIP")

    for theme_dir in theme_dirs():
        if theme_dir.name not in packaged:
            version = current_version(theme_dir)
            problems.append(f"{theme_dir.name}: no current release ZIP ships version {version!r}")


def check_readme_links(problems: list[str]) -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    for target in re.findall(r"\]\((releases/[^)]+|themes/[^)]+|previews/[^)]+)\)", text):
        if not (ROOT / target).exists():
            problems.append(f"README.md: broken link to {target}")
    for target in re.findall(r'<img src="([^"]+)"', text):
        if not (ROOT / target).exists():
            problems.append(f"README.md: broken image {target}")


def main() -> int:
    problems: list[str] = []
    themes = theme_dirs()

    keys: dict[str, str] = {}
    manifest_keys: dict[str, str] = {}
    for theme_dir in themes:
        key, manifest_key = check_theme(theme_dir, problems)
        for value, seen, label in ((key, keys, "ETHOS key"), (manifest_key, manifest_keys, "manifest key")):
            if value is None:
                continue
            if value in seen:
                problems.append(f"{theme_dir.name}: duplicate {label} {value!r} (also {seen[value]})")
            else:
                seen[value] = theme_dir.name

    check_releases(problems)
    check_readme_links(problems)

    if problems:
        print(f"FAILED â€” {len(problems)} problem(s) across {len(themes)} themes:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"OK â€” {len(themes)} themes, {len(list(RELEASES_ROOT.glob('*.zip')))} releases, all invariants hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
