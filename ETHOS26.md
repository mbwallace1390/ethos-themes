# ETHOS 26 compatibility

All 68 current themes target **ETHOS 26.1.0 and newer** on the existing 480px and 800px display layouts. Their API was checked against **26.1.2**, released September 10, 2026. FrSky describes that release as being for early adopters. [Official release](https://github.com/FrSkyRC/ETHOS-Feedback-Community/releases/tag/26.1.2)

The v1.2.0 collection introduced [readability and preview improvements](VISUAL_UPGRADE.md). Seven collection packages are v1.2.4 and the other 59 remain v1.2.3; Ink & Halo is v1.0.2 and uses the same contrast checks, responsive artwork, and native registration behavior. America 250 remains v1.2.1.

Each theme ZIP includes **784x50** artwork for 800px radios and **464x50** artwork for 480px radios, selected automatically. Current catalog previews show one header sample per theme using the larger artwork. They are desktop illustrations, not firmware screenshots; both native-size assets remain in every download.

## Targeted refinements: v1.2.4

Seven themes receive v1.2.4 packages:

- **Neon Horizon:** clips the horizontal sun stripes inside its outline and gives the perspective grid more depth while keeping the logo clear.
- **Royal Blue Strong and Desert Tactical:** strengthen selected-control outlines against the theme backgrounds.
- **Loom, Halftone, and Desert Tactical:** improve separation between the ETHOS logo and the continuous textured artwork.
- **RF Blue Pro and RF Suite Blue (Classic Blue in the catalog):** clarify that each is a standalone ETHOS radio theme. Their existing theme names, folders, artwork, and runtime behavior are preserved.

Check these details in both packaged toolbar sizes and on both radio sizes using [the testing checklist](TESTING.md). The single header sample in the catalog does not replace those checks.

The remaining 59 collection themes stay at v1.2.3; Ink & Halo stays at v1.0.2 and America 250 at v1.2.1. Previous ZIPs remain frozen snapshots. The changes add no recurring Lua drawing work.

## Continuous header artwork: v1.2.3

The 66 collection themes use continuous backgrounds and textures across each native toolbar width. Fine material detail remains visible through the transparent ETHOS logo; a flat rectangle no longer replaces the artwork at the center. Accent rails run below the wordmark, connected decorative paths bend around its lettering, and prominent illustrations sit beside it.

The design preserves each theme's palette, logo colors, controls, name, and runtime key. Only the static artwork layout changes; the radio still loads the background and logo during initialization without a recurring drawing task. Ink & Halo remains v1.0.2, and America 250 remains v1.2.1.

The updated previews illustrate these layouts using the shipped assets. Inspect both 480px and 800px layouts for continuous materials and lines, complete motifs, and readable logo lettering using [the testing checklist](TESTING.md). Desktop artwork checks do not establish firmware placement or physical-radio acceptance. Earlier ZIPs, including v1.2.2, remain frozen snapshots.

## Header artwork clearance: v1.2.2 and v1.0.2

Collection v1.2.2 moved motifs into left and right panels with a clear 160px center around the ETHOS logo. Version 1.2.3 supersedes that layout to restore continuous backgrounds and decorative paths; the v1.2.2 archives remain unchanged.

Ink & Halo v1.0.2 raised and widened its halo arc to leave a clear gap behind and around the baked-in wordmark at both display sizes. Its palette and transparent logo override were preserved, and this remains its current release. America 250's v1.2.1 artwork and hidden default logo remain unchanged.

## Collection logo update: v1.2.1

Version 1.2.1 added a transparent ETHOS `toolbarLogo` bitmap colored to match each of the 66 collection palettes. The small bitmap is requested once during initialization, with a protected load so an initialization failure still allows the palette and toolbar background to register. That update added no recurring drawing task and preserved the underlying toolbar artwork, palette, theme name, and runtime key. Its ZIPs remain frozen snapshots.

At that release, America 250 stayed at v1.2.1 with its logo hidden to protect the anniversary inscription, and Ink & Halo stayed at v1.0.1 with its wordmark baked into the halo artwork. Startup and About/Info branding remain unchanged for all themes; the documented API limits are explained below.

## America 250 header fix: v1.2.1

On the user's transmitter, the default ETHOS logo covered the America 250 inscription. This patch sets `toolbarLogo` to a packaged, fully transparent 1x1 PNG loaded once during initialization. ETHOS documents bitmap logo overrides and PNG transparency in its [26.1.2 Lua reference](https://github.com/FrSkyRC/ETHOS-Feedback-Community/releases/download/26.1.2/lua-doc.zip). A failed logo load still allows the palette and toolbar background to register.

In the original 67-theme review, all 134 toolbar images were checked at both native sizes. America 250 was the only theme with header text; the other 66 themes retained their existing logo behavior. Its palette, artwork, name, and runtime key were unchanged. The generator and Suite manifest include the transparent logo asset so regeneration and installation preserve the inscription.

## Ink & Halo header update: v1.0.1

Version 1.0.1 replaced Ink & Halo's toolbar inscription with a white and pale-blue ETHOS wordmark inside the halo. The wordmark was baked into both toolbar images, while the existing transparent `toolbarLogo` override prevented a second logo from appearing. The palette, theme name, runtime key, and initialization-only behavior stayed the same. The v1.0.0 and v1.0.1 ZIPs remain frozen snapshots.

Startup and About/Info branding remain unchanged. The [ETHOS 26.1.2 native-theme API](https://github.com/FrSkyRC/ETHOS-Feedback-Community/releases/download/26.1.2/lua-doc.zip) documents toolbar customization but no startup-logo or About/Info customization settings. FrSky's [Info documentation](https://ethos-doc.frsky-rc.com/system-setup/info/) describes the firmware information page. A [2022 developer explanation](https://github.com/FrSkyRC/ETHOS-Feedback-Community/issues/1339#issuecomment-1012032025) says startup occurs before the filesystem is mounted; that is historical context, not a verified ETHOS 26 customization method.

## What changed in theme package v1.1.0

- Corrected the ZIP layout for **Lua Library > Install from local .zip**: the manifest, `main.lua`, and toolbar images now sit at the archive root. Suite reads the manifest's `folder` to choose the destination under `scripts`. Older archives wrapped everything in that folder, which does not meet the current local-package specification. [FrSky package specification](https://github.com/FrSkyRC/ETHOS-Feedback-Community/blob/26.1.2/lua/frsky/ethos_lua_manifest.md)
- Preserved each theme's name, runtime key, package identity, palette, control style, and both toolbar images. Existing registration options and the 18-color order already matched FrSky's release-tag theme example. [Official example](https://github.com/FrSkyRC/ETHOS-Feedback-Community/blob/26.1.2/lua/themes/theme-dracula/main.lua)
- Skip theme initialization when firmware has no `system.registerTheme` function. This avoids a startup error on unsupported firmware; it does not add theme support to that firmware.
- Use the large image when display width is missing or not numeric. If `lcd.loadBitmap` raises an error during initialization or returns no handle, register the color theme without a custom toolbar background.
- Updated generators, manifests, installation instructions, and package checks so rebuilding preserves these changes. Previous release ZIPs remain frozen.

## Install or update

1. Download the theme's latest ZIP from the main catalog: **seven updated themes v1.2.4**, **59 collection themes v1.2.3**, **Ink & Halo v1.0.2**, or **America 250 v1.2.1**.
2. In Suite, use **Lua Library > Install from local .zip**, then select that ZIP.
3. Restart the transmitter and select the theme under **System > General > Theme**.

For manual installation, create the theme's named folder inside `scripts` and extract the ZIP **contents into that folder**. For Carbon, the result must be `scripts/theme-carbon/main.lua`, with the manifest and both toolbar PNGs beside it. Do not extract the loose files directly into `scripts`. Remove an old `main.luac` from that same theme folder when updating, so the firmware can compile the new source. Copying the complete source folder from this repository into `scripts` also works.

The manual install location and theme selection follow FrSky's [theme instructions](https://github.com/FrSkyRC/ETHOS-Feedback-Community/blob/26.1.2/lua/themes/README.md). Old, folder-wrapped ZIPs are retained for manual installation only; use the current catalog links for the Suite workflow.

To roll back a theme, copy its previous complete folder back under `scripts`, remove that folder's compiled `main.luac`, and restart. This does not roll back transmitter firmware.

## Verification and limits

The checks execute all themes with documented API stubs in Lua 5.2 and 5.4, cover both display widths, absent width, unsupported firmware, and bitmap initialization failures, and execute the packaged Lua. Package checks verify complete files, installer selectors, stable unique identities, and byte equality with sources.

`lcd.loadBitmap` defaults to lazy loading. The protected call only covers initialization; it cannot catch a later firmware decoding error. PNG structure and dimensions are checked on the desktop. These API facts were checked in the [26.1.2 Lua reference](https://github.com/FrSkyRC/ETHOS-Feedback-Community/releases/download/26.1.2/lua-doc.zip).

The America 250 v1.2.1 source and all three PNGs additionally passed native bitmap decoding and theme registration in the [official X20 26.1.2 WebSimulator](https://github.com/FrSkyRC/ETHOS-Feedback-Community/releases/download/26.1.2/X20-FCC-WebSimulator.zip), without Lua errors. This check did not visually inspect the simulator screen or the physical radio. Complete [TESTING.md](TESTING.md) on the target transmitter before treating the fix as radio-validated. Rotorflight and RF Suite source files are not part of this repository update.
