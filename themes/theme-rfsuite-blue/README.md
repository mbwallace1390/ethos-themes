# RF Suite Blue

Stable version: 1.0.3

RF Suite Blue is a dark FrSky ETHOS theme that changes the selected-control highlight from yellow to blue. It has been confirmed to improve the selected Rotorflight RF Suite menu tiles.

## Compatibility

The internal theme key is `RFBlue`, which is six characters long. FrSky supplied themes use short internal keys, and this corrected key allows the theme to appear in the ETHOS theme list.

## Installation

Copy the complete `theme-rfsuite-blue` folder into the transmitter `scripts` directory, restart the transmitter, and select **RF Suite Blue** under **System > General > Theme**.

Expected files:

```text
scripts/theme-rfsuite-blue/main.lua
scripts/theme-rfsuite-blue/ethos_lua_manifest.json
scripts/theme-rfsuite-blue/toolbar-rfsuite-blue.png
```

The release omits `main.luac` so ETHOS can create a fresh compiled copy from the corrected source.
