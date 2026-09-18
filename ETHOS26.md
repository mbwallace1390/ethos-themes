# ETHOS 26 compatibility

All 68 current themes target **ETHOS 26.1.0 and newer** on the existing 480px and 800px display layouts. Their API was checked against **26.1.2**, released September 10, 2026. FrSky describes that release as being for early adopters. [Official release](https://github.com/FrSkyRC/ETHOS-Feedback-Community/releases/tag/26.1.2)

The v1.2.0 collection includes [readability and preview improvements](VISUAL_UPGRADE.md). Ink & Halo joins the catalog at v1.0.0 with the same contrast checks, responsive artwork, and native registration behavior.

## America 250 header fix: v1.2.1

On the user's transmitter, the default ETHOS logo covered the America 250 inscription. This patch sets `toolbarLogo` to a packaged, fully transparent 1x1 PNG loaded once during initialization. ETHOS documents bitmap logo overrides and PNG transparency in its [26.1.2 Lua reference](https://github.com/FrSkyRC/ETHOS-Feedback-Community/releases/download/26.1.2/lua-doc.zip). A failed logo load still allows the palette and toolbar background to register.

In the original 67-theme review, all 134 toolbar images were checked at both native sizes. America 250 was the only theme with header text; the other 66 themes retained their existing logo behavior. Its palette, artwork, name, and runtime key were unchanged. Ink & Halo now uses the same transparent logo override for its header inscription. Both generators and Suite manifests include the logo asset so regeneration and installation preserve the text.

## What changed in theme package v1.1.0

- Corrected the ZIP layout for **Lua Library > Install from local .zip**: the manifest, `main.lua`, and toolbar images now sit at the archive root. Suite reads the manifest's `folder` to choose the destination under `scripts`. Older archives wrapped everything in that folder, which does not meet the current local-package specification. [FrSky package specification](https://github.com/FrSkyRC/ETHOS-Feedback-Community/blob/26.1.2/lua/frsky/ethos_lua_manifest.md)
- Preserved each theme's name, runtime key, package identity, palette, control style, and both toolbar images. Existing registration options and the 18-color order already matched FrSky's release-tag theme example. [Official example](https://github.com/FrSkyRC/ETHOS-Feedback-Community/blob/26.1.2/lua/themes/theme-dracula/main.lua)
- Skip theme initialization when firmware has no `system.registerTheme` function. This avoids a startup error on unsupported firmware; it does not add theme support to that firmware.
- Use the large image when display width is missing or not numeric. If `lcd.loadBitmap` raises an error during initialization or returns no handle, register the color theme without a custom toolbar background.
- Updated generators, manifests, installation instructions, and package checks so rebuilding preserves these changes. Previous release ZIPs remain frozen.

## Install or update

1. Download the theme's latest ZIP from the main catalog: **America 250 v1.2.1**, **Ink & Halo v1.0.0**, or **v1.2.0** for the remaining themes.
2. In Suite, use **Lua Library > Install from local .zip**, then select that ZIP.
3. Restart the transmitter and select the theme under **System > General > Theme**.

For manual installation, create the theme's named folder inside `scripts` and extract the ZIP **contents into that folder**. For Carbon, the result must be `scripts/theme-carbon/main.lua`, with the manifest and both toolbar PNGs beside it. Do not extract the loose files directly into `scripts`. Remove an old `main.luac` from that same theme folder when updating, so the firmware can compile the new source. Copying the complete source folder from this repository into `scripts` also works.

The manual install location and theme selection follow FrSky's [theme instructions](https://github.com/FrSkyRC/ETHOS-Feedback-Community/blob/26.1.2/lua/themes/README.md). Old, folder-wrapped ZIPs are retained for manual installation only; use the current catalog links for the Suite workflow.

To roll back a theme, copy its previous complete folder back under `scripts`, remove that folder's compiled `main.luac`, and restart. This does not roll back transmitter firmware.

## Verification and limits

The checks execute all themes with documented API stubs in Lua 5.2 and 5.4, cover both display widths, absent width, unsupported firmware, and bitmap initialization failures, and execute the packaged Lua. Package checks verify complete files, installer selectors, stable unique identities, and byte equality with sources.

`lcd.loadBitmap` defaults to lazy loading. The protected call only covers initialization; it cannot catch a later firmware decoding error. PNG structure and dimensions are checked on the desktop. These API facts were checked in the [26.1.2 Lua reference](https://github.com/FrSkyRC/ETHOS-Feedback-Community/releases/download/26.1.2/lua-doc.zip).

The America 250 v1.2.1 source and all three PNGs additionally passed native bitmap decoding and theme registration in the [official X20 26.1.2 WebSimulator](https://github.com/FrSkyRC/ETHOS-Feedback-Community/releases/download/26.1.2/X20-FCC-WebSimulator.zip), without Lua errors. This check did not visually inspect the simulator screen or the physical radio. Complete [TESTING.md](TESTING.md) on the target transmitter before treating the fix as radio-validated. Rotorflight and RF Suite source files are not part of this repository update.
