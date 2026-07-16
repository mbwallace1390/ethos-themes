"""Shared helper to losslessly shrink generated PNGs with optipng.

This only runs at asset-generation time on a maintainer's machine (via the
generate_*.py / add_x18_support_all_themes.py scripts) -- it never runs on
the radio. Pillow's own `optimize=True` leaves noticeable bytes on the
table compared to optipng's exhaustive filter/strategy search, so we run
optipng as a lossless post-process step right after each PNG is saved.

If optipng isn't installed, generation still succeeds; you'll just get
Pillow-only compression until it's available (`apt install optipng` /
`brew install optipng`).
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

_OPTIPNG = shutil.which("optipng")
_WARNED = False


def optimize_png(path: Path) -> None:
    """Losslessly recompress a PNG in place with optipng, if available."""
    global _WARNED
    if _OPTIPNG is None:
        if not _WARNED:
            print("optipng not found on PATH; skipping extra PNG optimization "
                  "(install optipng for smaller output files).")
            _WARNED = True
        return
    subprocess.run(
        [_OPTIPNG, "-o7", "-quiet", str(path)],
        check=True,
    )
