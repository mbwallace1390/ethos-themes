"""Build-time contrast checks for the literal 18-color ETHOS theme palette.

The radio receives ordinary RGB literals. These desktop-only helpers preserve
the theme's backgrounds, accents, and artwork while adjusting deficient text.
"""

from __future__ import annotations

import re
from collections.abc import Mapping

RGB = tuple[int, int, int]
ROLES = (
    "PRIMARY_COLOR", "SECONDARY_BGCOLOR", "HIGHLIGHT_COLOR",
    "HIGHLIGHT_CONTRASTING_COLOR", "DISABLE_COLOR", "PRIMARY_BGCOLOR",
    "OVERLAY_COLOR", "SECONDARY_COLOR", "SAFE_COLOR", "PAGE_BGCOLOR",
    "ERROR_COLOR", "ACTIVE_COLOR", "INACTIVE_COLOR",
    "BUTTON_BORDER_ACTIVE_COLOR", "BUTTON_BORDER_COLOR", "WARNING_COLOR",
    "SAFE_CONTRASTING_COLOR", "TOPLCD_BGCOLOR",
)
SURFACES = ("PRIMARY_BGCOLOR", "SECONDARY_BGCOLOR", "PAGE_BGCOLOR")
# Disabled controls are exempt from WCAG; 3:1 is a voluntary design target.
TARGETS = {
    "PRIMARY_COLOR": (4.5, SURFACES),
    "SECONDARY_COLOR": (4.5, SURFACES),
    "HIGHLIGHT_CONTRASTING_COLOR": (4.5, ("HIGHLIGHT_COLOR",)),
    "SAFE_CONTRASTING_COLOR": (4.5, ("SAFE_COLOR",)),
    "ACTIVE_COLOR": (4.5, SURFACES),
    "INACTIVE_COLOR": (4.5, SURFACES),
    "DISABLE_COLOR": (3.0, SURFACES),
}


def _rgb(value: RGB) -> RGB:
    if (not isinstance(value, (tuple, list)) or len(value) != 3
            or any(type(channel) is not int or not 0 <= channel <= 255
                   for channel in value)):
        raise ValueError(f"Expected three integer RGB channels in 0..255: {value!r}")
    return tuple(value)


def _luminance(color: RGB) -> float:
    # WCAG relative luminance: linearize sRGB before weighting its channels.
    channels = [channel / 255 for channel in color]
    linear = [channel / 12.92 if channel <= 0.04045
              else ((channel + 0.055) / 1.055) ** 2.4 for channel in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(first: RGB, second: RGB) -> float:
    """Return the WCAG relative-luminance ratio for two opaque sRGB colors."""
    light, dark = sorted((_luminance(_rgb(first)), _luminance(_rgb(second))), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def _blend_candidates(color: RGB, endpoint: int):
    # Visit every distinct integer RGB color along a blend toward black/white.
    # Channel rounding changes at these half-integer boundaries. Sampling each
    # interval avoids arbitrary blend steps and finds the smallest viable edit.
    boundaries = {0.0, 1.0}
    for channel in color:
        distance = abs(endpoint - channel)
        boundaries.update((step + 0.5) / distance for step in range(distance))
    boundaries = sorted(boundaries)
    previous = color
    for left, right in zip(boundaries, boundaries[1:]):
        amount = (left + right) / 2
        candidate = tuple(int(channel + (endpoint - channel) * amount + 0.5)
                          for channel in color)
        if candidate != previous:
            yield candidate
            previous = candidate


def _improve(color: RGB, backgrounds: tuple[RGB, ...], target: float) -> RGB:
    def passes(candidate: RGB) -> bool:
        return all(contrast_ratio(candidate, background) >= target
                   for background in backgrounds)

    if passes(color):
        return color
    choices = []
    for endpoint in (0, 255):
        for candidate in _blend_candidates(color, endpoint):
            if passes(candidate):
                # RGB movement grows monotonically on either blend direction.
                choices.append(candidate)
                break
    if not choices:
        raise ValueError(f"No black/white blend of {color} reaches {target}:1 on {backgrounds}")
    return min(choices, key=lambda candidate: sum((a - b) ** 2
                                                 for a, b in zip(color, candidate)))


def polish_palette(palette: Mapping[str, RGB]) -> dict[str, RGB]:
    """Return a new 18-role palette; alter only foregrounds below their target.

    Among integer sRGB blends toward black or white, choose the least squared
    RGB movement that passes on every relevant background. Preserve good colors.
    """
    if set(palette) != set(ROLES):
        raise ValueError("Palette must contain exactly the 18 documented ETHOS color roles")
    result = {role: _rgb(palette[role]) for role in ROLES}
    for role, (target, surfaces) in TARGETS.items():
        result[role] = _improve(result[role], tuple(result[surface] for surface in surfaces), target)
    return result


_BLOCK = re.compile(r"^[ \t]*colors[ \t]*=[ \t]*\{[ \t]*\r?\n(?P<body>.*?)"
                    r"^[ \t]*\},?[ \t]*\r?$", re.MULTILINE | re.DOTALL)
_CHANNEL = r"(?:0[xX][0-9a-fA-F]+|[0-9]+)"
_RGB_LITERAL = re.compile(rf"lcd\.RGB\([ \t]*({_CHANNEL})[ \t]*,[ \t]*"
                          rf"({_CHANNEL})[ \t]*,[ \t]*({_CHANNEL})[ \t]*\)")
_ENTRY = re.compile(rf"[ \t]*(?P<value>lcd\.RGB\([ \t]*{_CHANNEL}[ \t]*,[ \t]*"
                    rf"{_CHANNEL}[ \t]*,[ \t]*{_CHANNEL}[ \t]*\)|COLOR_BLACK)"
                    r"[ \t]*,[ \t]*--[ \t]*(?P<role>[A-Z_]+)\b[^\r\n]*(?:\r?\n)?")


def polish_lua_source(source: str) -> str:
    """Polish only a complete literal, role-commented colors array; never run Lua.

    Reject unknown/computed entries, duplicated roles, and changed role order
    rather than guessing at arbitrary source. Keep all other code and comments.
    """
    blocks = list(_BLOCK.finditer(source))
    if len(blocks) != 1:
        raise ValueError("Expected one literal ETHOS colors array")
    block = blocks[0]
    entries = []
    palette = {}
    rows = block.group("body").splitlines(keepends=True)
    for row in rows:
        if not row.strip():
            entries.append(None)
            continue
        entry = _ENTRY.fullmatch(row)
        if entry is None:
            raise ValueError("Palette entries must be RGB literals or COLOR_BLACK with role comments")
        role, value = entry.group("role", "value")
        if len(palette) >= len(ROLES) or role != ROLES[len(palette)]:
            raise ValueError("Palette role comments must match the 18 documented positions")
        if value == "COLOR_BLACK":
            if role in TARGETS:
                raise ValueError("Foreground roles must use RGB literals; named colors are preserved")
            color = (0, 0, 0)
        else:
            color = tuple(int(channel, 16 if channel.lower().startswith("0x") else 10)
                          for channel in _RGB_LITERAL.fullmatch(value).groups())
        palette[role] = _rgb(color)
        entries.append(entry)
    polished = polish_palette(palette)
    for index, entry in enumerate(entries):
        if entry is None:
            continue
        role = entry.group("role")
        if polished[role] != palette[role]:
            red, green, blue = polished[role]
            value = f"lcd.RGB(0x{red:02X}, 0x{green:02X}, 0x{blue:02X})"
            rows[index] = rows[index][:entry.start("value")] + value + rows[index][entry.end("value"):]
    return source[:block.start("body")] + "".join(rows) + source[block.end("body"):]
