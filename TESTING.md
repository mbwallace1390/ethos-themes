# Theme Testing Checklist

Use this checklist before marking a theme as ready.

## Automated checks

From the repository root, using Python 3.12 or newer:

```powershell
python -m pip install -r tools/requirements-dev.txt
python -m unittest discover -s tools -p "test_*.py" -v
python tools/validate_catalog.py
```

GitHub Actions runs **Validate ETHOS themes** for every push to `main` and pull request targeting `main`. It can also be run manually.

For a full rebuild on GitHub, run **Generate ETHOS theme artifacts** from Actions. It generates all families, previews, and current ZIPs, runs the same checks, and attaches a downloadable artifact for review. It does not commit or push files. Preview font versions and optional PNG compression tools can affect output bytes, so review generated artifacts before publishing them.

After changing theme sources locally, regenerate the current ETHOS Suite-compatible ZIPs:

```powershell
python tools/rebuild_releases.py
python tools/generate_all_previews.py
```

Then rerun the checks. They cover 67 themes, both 480px and 800px artwork choices, full PNG decoding, required manifest fields, all 18 color roles, Lua 5.2/5.4 parsing and initialization, unsupported firmware, failed bitmap initialization, and complete current ZIP contents. Historical ZIPs are retained as snapshots. These tests use API stubs and do not run the actual ETHOS firmware.

## ETHOS 26 installation

- Use ETHOS 26.1.0 or newer; record the exact build (API reference: 26.1.2).
- Install the current ZIP through ETHOS Suite's local ZIP installer; confirm it is recognized and targets `scripts/<theme-folder>` (America 250 v1.2.1, other themes v1.2.0).
- Check that manual extraction into that same folder also gives `scripts/<theme-folder>/main.lua` with both toolbar images beside it.
- Remove that theme folder's previous `main.luac` when updating; restart and confirm the theme remains selectable.
- Check **System > Information** for Lua errors after restart and after selecting the theme.

## ETHOS interface

- Theme appears in **System > General > Theme**.
- America 250: the header inscription stays visible without the default ETHOS logo over it; verify both display widths and confirm `logo-transparent.png` was installed.
- Selected menu entries use the intended highlight color.
- Text remains readable on highlighted controls.
- Disabled controls remain visibly different from enabled controls.
- Warnings, errors, and safe-state colors remain recognizable.

## Devices

Record the tested ETHOS version and transmitter model in the theme's README before release.

The catalog has desktop API/package checks. America 250 v1.2.1 also passed bitmap decoding and source registration in the official X20 26.1.2 WebSimulator; this was not a visual simulator test. Real-radio acceptance, Suite installer UI acceptance, and screen readability must be recorded separately. Check both a standard 480px X18 and an 800px transmitter if claiming both device layouts are verified.
