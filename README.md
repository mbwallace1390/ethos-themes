# ETHOS Themes

Custom themes for FrSky ETHOS, with an initial focus on improving the appearance and readability of Rotorflight RF Suite.

## Stable theme

### RF Suite Blue v1.0.3

Location: [`themes/theme-rfsuite-blue`](themes/theme-rfsuite-blue)

RF Suite Blue replaces the yellow selected-control highlight with a clearer blue highlight. It has been tested successfully on an ETHOS transmitter and confirmed to change the selected Rotorflight RF Suite menu tiles from yellow to blue.

The working build uses the short internal ETHOS theme key `RFBlue`. FrSky's supplied themes use internal keys of seven characters or fewer, and longer keys may cause a theme to be silently omitted from the theme list.

## Requirements

- FrSky ETHOS 26.1 or newer with Lua theme support
- A compatible ETHOS transmitter or the ETHOS simulator

## Installation

1. Download [`RF-Suite-Blue-v1.0.3.zip`](releases/RF-Suite-Blue-v1.0.3.zip).
2. Install it through ETHOS Suite, or extract it manually.
3. For a manual installation, copy the complete `theme-rfsuite-blue` folder into the transmitter's `scripts` directory.
4. Restart the transmitter.
5. Open **System → General → Theme** and select **RF Suite Blue**.

The installed files should appear at:

```text
scripts/theme-rfsuite-blue/main.lua
scripts/theme-rfsuite-blue/ethos_lua_manifest.json
scripts/theme-rfsuite-blue/toolbar-rfsuite-blue.png
```

`main.luac` is intentionally not distributed. ETHOS creates a fresh compiled copy from `main.lua`.

## Repository structure

```text
ethos-themes/
├── README.md
├── TESTING.md
├── releases/
│   └── RF-Suite-Blue-v1.0.3.zip
└── themes/
    └── theme-rfsuite-blue/
        ├── README.md
        ├── ethos_lua_manifest.json
        ├── main.lua
        └── toolbar-rfsuite-blue.png
```
