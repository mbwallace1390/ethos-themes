# ETHOS Themes

Custom themes and interface experiments for FrSky ETHOS, with an initial focus on improving the appearance and readability of Rotorflight RF Suite.

## Themes

### RF Suite Blue Test

Location: [`themes/theme-rfsuite-blue-test`](themes/theme-rfsuite-blue-test)

This first theme replaces the yellowish selected-control highlight with a deep blue highlight. It is intended to confirm that RF Suite's standard menu tiles inherit their selected appearance from the active ETHOS system theme.

## Requirements

- FrSky ETHOS 26.1 or newer with Lua theme support
- A compatible ETHOS transmitter or the ETHOS simulator

## Installing a theme

1. Download or clone this repository.
2. Open the desired folder under `themes`.
3. Copy that complete theme folder into the transmitter's `scripts` directory.
4. On the transmitter, open **System → General → Theme**.
5. Select the installed theme.

Example installed path:

```text
scripts/theme-rfsuite-blue-test/main.lua
```

## Project status

The included theme is currently a test build. Results should be verified in the ETHOS simulator and on a transmitter before treating it as a finished release.

## Repository structure

```text
ethos-themes/
├── README.md
├── TESTING.md
└── themes/
    └── theme-rfsuite-blue-test/
        ├── README.md
        └── main.lua
```
