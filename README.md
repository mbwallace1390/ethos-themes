# ETHOS Themes

Custom themes for FrSky ETHOS, focused on improving Rotorflight RF Suite.

## Stable theme

### RF Suite Blue v1.0.4

Stable source: [`themes/theme-rfsuite-blue`](themes/theme-rfsuite-blue)

Version 1.0.4 keeps the working `RFBlue` key, uses a thinner 784x50 toolbar gradient, and changes the page background to blue-black so ETHOS's fixed side margins blend into the layout.

## Installation

1. Open [`themes/theme-rfsuite-blue`](themes/theme-rfsuite-blue).
2. Copy the complete `theme-rfsuite-blue` folder into the transmitter's `scripts` folder.
3. Restart the transmitter.
4. Select **RF Suite Blue** under **System > General > Theme**.

Expected files:

```text
scripts/theme-rfsuite-blue/main.lua
scripts/theme-rfsuite-blue/ethos_lua_manifest.json
scripts/theme-rfsuite-blue/toolbar-rfsuite-blue.png
```

`main.luac` is intentionally omitted so ETHOS creates a fresh compiled copy.

Previous packaged release: [`v1.0.3`](releases/RF-Suite-Blue-v1.0.3.zip)
