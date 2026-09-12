"""Repackage every theme's current release ZIP from its source folder.

The generators already repackage the themes they own, but a few themes are
hand-maintained and have no generator. Run this after editing any theme folder
so the downloadable ZIP never drifts from the committed sources. Superseded
archives (a v1.0.3 ZIP kept beside the current v1.0.5) are left untouched.
"""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

from theme_lib import RELEASES_ROOT, THEMES_ROOT, write_release

VERSION_RE = re.compile(r"-v(\d+\.\d+\.\d+)\.zip$")


def releases_by_theme() -> dict[str, list[Path]]:
    mapping: dict[str, list[Path]] = {}
    for release in sorted(RELEASES_ROOT.glob("*.zip")):
        try:
            with zipfile.ZipFile(release) as archive:
                if "ethos_lua_manifest.json" in archive.namelist():
                    manifest = json.loads(archive.read("ethos_lua_manifest.json"))
                    roots = {manifest.get("folder", "")}
                else:
                    roots = {n.split("/", 1)[0] for n in archive.namelist() if "/" in n}
        except zipfile.BadZipFile:
            continue
        folders = [r for r in roots if (THEMES_ROOT / r).is_dir()]
        if len(folders) == 1:
            mapping.setdefault(folders[0], []).append(release)
    return mapping


def main() -> None:
    rebuilt = skipped = 0
    for folder, releases in sorted(releases_by_theme().items()):
        theme_dir = THEMES_ROOT / folder
        manifest = theme_dir / "ethos_lua_manifest.json"
        version = None
        if manifest.exists():
            version = json.loads(manifest.read_text(encoding="utf-8")).get("version")

        # Retain the established download name but advance its version. Older
        # archives remain immutable snapshots, including their original layout.
        current = [p for p in releases if VERSION_RE.search(p.name)
                   and VERSION_RE.search(p.name).group(1) == version]
        if not current:
            latest = max(releases, key=lambda p: tuple(map(int, VERSION_RE.search(p.name).group(1).split("."))))
            current = [latest.with_name(VERSION_RE.sub(f"-v{version}.zip", latest.name))]
        for release in current:
            write_release(theme_dir, release)
            rebuilt += 1
        skipped += sum(p not in current for p in releases)

    print(f"Rebuilt {rebuilt} current release ZIPs, left {skipped} superseded archive(s) untouched")


if __name__ == "__main__":
    main()
