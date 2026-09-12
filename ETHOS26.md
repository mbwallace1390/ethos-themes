# ETHOS 26 compatibility

All 67 current themes target **ETHOS 26.1.0 and newer** on the existing 480px and 800px display layouts. Their API was checked against **26.1.2**, released September 10, 2026. FrSky describes that release as being for early adopters. [Official release](https://github.com/FrSkyRC/ETHOS-Feedback-Community/releases/tag/26.1.2)

The current v1.2.0 catalog also includes [readability and preview improvements](VISUAL_UPGRADE.md).

## What changed in theme package v1.1.0

- Corrected the ZIP layout for **Lua Library > Install from local .zip**: the manifest, `main.lua`, and toolbar images now sit at the archive root. Suite reads the manifest's `folder` to choose the destination under `scripts`. Older archives wrapped everything in that folder, which does not meet the current local-package specification. [FrSky package specification](https://github.com/FrSkyRC/ETHOS-Feedback-Community/blob/26.1.2/lua/frsky/ethos_lua_manifest.md)
- Preserved each theme's name, runtime key, package identity, palette, control style, and both toolbar images. Existing registration options and the 18-color order already matched FrSky's release-tag theme example. [Official example](https://github.com/FrSkyRC/ETHOS-Feedback-Community/blob/26.1.2/lua/themes/theme-dracula/main.lua)
- Skip theme initialization when firmware has no `system.registerTheme` function. This avoids a startup error on unsupported firmware; it does not add theme support to that firmware.
- Use the large image when display width is missing or not numeric. If `lcd.loadBitmap` raises an error during initialization or returns no handle, register the color theme without a custom toolbar background.
- Updated generators, manifests, installation instructions, and package checks so rebuilding preserves these changes. Previous release ZIPs remain frozen.

## Install or update

1. Download the theme's **v1.2.0** ZIP from the main catalog.
2. In Suite, use **Lua Library > Install from local .zip**, then select that ZIP.
3. Restart the transmitter and select the theme under **System > General > Theme**.

For manual installation, create the theme's named folder inside `scripts` and extract the ZIP **contents into that folder**. For Carbon, the result must be `scripts/theme-carbon/main.lua`, with the manifest and both toolbar PNGs beside it. Do not extract the loose files directly into `scripts`. Remove an old `main.luac` from that same theme folder when updating, so the firmware can compile the new source. Copying the complete source folder from this repository into `scripts` also works.

The manual install location and theme selection follow FrSky's [theme instructions](https://github.com/FrSkyRC/ETHOS-Feedback-Community/blob/26.1.2/lua/themes/README.md). Old, folder-wrapped ZIPs are retained for manual installation only; use v1.2.0 for the current Suite workflow.

To roll back a theme, copy its previous complete folder back under `scripts`, remove that folder's compiled `main.luac`, and restart. This does not roll back transmitter firmware.

## Verification and limits

The checks execute all themes with documented API stubs in Lua 5.2 and 5.4, cover both display widths, absent width, unsupported firmware, and bitmap initialization failures, and execute the packaged Lua. Package checks verify complete files, installer selectors, stable unique identities, and byte equality with sources.

`lcd.loadBitmap` defaults to lazy loading. The protected call only covers initialization; it cannot catch a later firmware decoding error. PNG structure and dimensions are checked on the desktop. These API facts were checked in the [26.1.2 Lua reference](https://github.com/FrSkyRC/ETHOS-Feedback-Community/releases/download/26.1.2/lua-doc.zip).

These are desktop checks, not a physical-radio or official-simulator test. Complete [TESTING.md](TESTING.md) on the target transmitter before treating the release as radio-validated. Rotorflight and RF Suite source files are not part of this repository update.
