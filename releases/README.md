# Releases

## Current catalog

Every current ZIP includes an individual `preview.png` at the archive root. Extract the download on your computer and open the image to see the theme before installing it. These are illustrations made from the theme's artwork and colors, not firmware screenshots.

The current packages are **66 collection themes v1.2.5**, [America 250 v1.2.2](America-250-v1.2.2.zip), [Ink & Halo v1.0.3](Ink-and-Halo-v1.0.3.zip), [Copperline v1.0.1](Copperline-v1.0.1.zip), [Stormfront v1.0.1](Stormfront-v1.0.1.zip), and [Night Current v1.0.1](Night-Current-v1.0.1.zip). This packaging-only update preserves the installed themes' code, palettes, native artwork, and identities. It adds 71 ZIPs while preserving all 413 earlier archives unchanged, for 484 ZIPs in total.

All 71 themes target ETHOS 26.1.0 and newer, with API checks against 26.1.2. Choose a theme from the [main catalog](../README.md) for its individual ZIP. Physical-radio and Suite installer UI acceptance remain separate checks.

Current ZIPs use the root manifest layout required by **Lua Library > Install from local .zip**. The manifest excludes `preview.png`, so ETHOS Suite does not install it on the radio. For manual installation, extract the contents into `scripts/<theme-folder>/`; you may omit the preview. See [compatibility and installation](../ETHOS26.md).

## Earlier artwork updates

[Copperline v1.0.0](Copperline-v1.0.0.zip), [Stormfront v1.0.0](Stormfront-v1.0.0.zip), and [Night Current v1.0.0](Night-Current-v1.0.0.zip) introduced three standalone designs with static artwork, matching ETHOS logos, and both native toolbar sizes. See [the new-theme notes](../ETHOS26.md#copperline-stormfront-and-night-current-v100) and the [catalog preview](../previews/new-designs.png).

Seven collection themes received **v1.2.4**: Neon Horizon, Royal Blue Strong, Desert Tactical, Loom, Halftone, RF Blue Pro, and RF Suite Blue (Classic Blue in the catalog). That update fixed Neon Horizon's sun stripes and improved its grid depth, strengthened selected-control outlines and textured-header logo readability in the named themes, and clarified the two Blue themes' standalone purpose. Catalog previews show one header sample per theme; every download retains both native artwork sizes. See [the per-theme changes](../ETHOS26.md#targeted-refinements-v124).

At that release, the other **59 collection themes stayed at v1.2.3**. Continuous toolbar materials and theme identities were preserved across the collection, with no blank logo panel or recurring Lua drawing task. Those ZIPs remain frozen snapshots, including the previous v1.2.3 packages for the seven updated themes.

America 250 [v1.2.1](America-250-v1.2.1.zip) hid the default ETHOS logo over its anniversary inscription. [Ink & Halo v1.0.2](Ink-and-Halo-v1.0.2.zip) raised and widened its halo arc to leave a clear gap around the white and pale-blue ETHOS wordmark. Its [v1.0.0 ZIP](Ink-and-Halo-v1.0.0.zip) and [v1.0.1 ZIP](Ink-and-Halo-v1.0.1.zip) are also preserved. See [artwork changes](../ETHOS26.md#continuous-header-artwork-v123). Startup and About/Info branding remain unchanged for all themes; see [native-theme limits](../ETHOS26.md#ink--halo-header-update-v101).

Older archives below are preserved snapshots for manual installation. Their previous radio-test notes do not constitute validation of the current packages on ETHOS 26.

## RF Suite Blue v1.0.3

- Historical status: confirmed working on its original tested setup
- Package: [`RF-Suite-Blue-v1.0.3.zip`](RF-Suite-Blue-v1.0.3.zip)
- Notes: [`v1.0.3.md`](v1.0.3.md)

This is the first confirmed working release. It appears in the ETHOS theme selector and changes Rotorflight RF Suite selected menu tiles from yellow to blue.
