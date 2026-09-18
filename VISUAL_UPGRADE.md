# Theme readability update: v1.2.0

This records the original 67-theme v1.2.0 update. Later additions and package versions are listed in the [current catalog](README.md).

America 250 leads the preview catalog. All 67 themes have source-driven previews. The 66 collection cards now have larger layouts with selected, normal, active, disabled, highlight-text, and safe-state examples. RF Suite Blue also has its own preview. The commemorative America 250 image retains its dedicated layout.

## Radio appearance

The update adjusts 142 foreground colors across 66 themes. Backgrounds, accent fills, artwork, theme keys, and rounded/square control styles retain their existing identities. Values that already meet the chosen readability targets remain unchanged.

| Foreground role | Design target | Themes needing adjustment |
| --- | --- | ---: |
| Primary text on page/panels | 4.5:1 | 0 |
| Secondary text on page/panels | 4.5:1 | 1 |
| Text on highlighted controls | 4.5:1 | 11 |
| Text on safe-state backgrounds | 4.5:1 | 4 |
| Active labels on page/panels | 4.5:1 | 10 |
| Inactive labels on page/panels | 4.5:1 | 63 |
| Disabled labels on page/panels | 3:1 | 53 |

These are measured sRGB contrast targets for the source palettes. The 4.5:1 text target follows the [W3C contrast guidance](https://www.w3.org/TR/WCAG22/#contrast-minimum). Disabled controls are formally exempt; their 3:1 target here is a voluntary readability choice. Palette measurements alone do not establish WCAG compliance or real-radio visibility. Active and inactive colors receive the text target because applications can use them for labels as well as indicators.

Color adjustments happen in the Python generators. The radio still receives 18 literal color values and performs no contrast calculations or new background work. A common writer applies the same rules to future regeneration; tests reject missing or duplicate roles and check that a second polish pass makes no further changes.

## Preview improvements

The old preview helpers tried Linux-only font paths and fell back to the same tiny font for every requested size on Windows. The new renderer supports Windows and Linux fonts, honors heading/label sizes, uses ASCII fallback-safe captions, and reads colors from the current Lua files. Previews are illustrative controls with actual toolbar artwork; they are not firmware screenshots.

## Performance findings

All 134 toolbar images remain indexed PNGs, totaling 120,735 bytes. Tested recompression options offered no smaller pixel-identical indexed files, so the radio artwork is preserved. Lua remains initialization-only, with lazy bitmap loading and no recurring theme callbacks. No transmitter speed or RAM improvement is claimed.

## Packages and validation

The update released all 67 Suite packages at v1.2.0. Earlier archives remain available. The automated checks cover palette targets, both display widths, Lua 5.2/5.4 initialization, bitmap failure handling, complete manifests, and exact archive/source contents. See [TESTING.md](TESTING.md) for commands and the remaining physical-radio checks.
