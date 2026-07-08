# ETHOS Themes

Custom FrSky ETHOS themes focused on improving Rotorflight RF Suite.

## RF Pro collection

All RF Pro themes use dark square controls, outline focus, clear inactive and disabled states, and a lightweight 784x50 toolbar. Every theme has a separate short ETHOS-safe key, so they can remain installed together.

### Available themes

- **RF Blue Pro v1.0.0** — [Download](releases/RF-Blue-Pro-v1.0.0.zip) — [Source](themes/theme-rfblue-pro)
- **RF Violet Pro v1.0.0** — [Download](releases/RF-Violet-Pro-v1.0.0.zip) — [Source](themes/theme-rf-violet-pro)
- **RF Emerald Pro v1.0.0** — [Download](releases/RF-Emerald-Pro-v1.0.0.zip) — [Source](themes/theme-rf-emerald-pro)
- **RF Ember Pro v1.0.0** — [Download](releases/RF-Ember-Pro-v1.0.0.zip) — [Source](themes/theme-rf-ember-pro)
- **RF Magenta Pro v1.0.0** — [Download](releases/RF-Magenta-Pro-v1.0.0.zip) — [Source](themes/theme-rf-magenta-pro)
- **RF Cyan Pro v1.0.0** — [Download](releases/RF-Cyan-Pro-v1.0.0.zip) — [Source](themes/theme-rf-cyan-pro)
- **RF Crimson Pro v1.0.0** — [Download](releases/RF-Crimson-Pro-v1.0.0.zip) — [Source](themes/theme-rf-crimson-pro)
- **RF Gold Pro v1.0.0** — [Download](releases/RF-Gold-Pro-v1.0.0.zip) — [Source](themes/theme-rf-gold-pro)
- **RF Teal Pro v1.0.0** — [Download](releases/RF-Teal-Pro-v1.0.0.zip) — [Source](themes/theme-rf-teal-pro)
- **RF Lime Pro v1.0.0** — [Download](releases/RF-Lime-Pro-v1.0.0.zip) — [Source](themes/theme-rf-lime-pro)

## Classic theme

**RF Suite Blue v1.0.4** keeps rounded controls and solid blue selected controls.

- [View source](themes/theme-rfsuite-blue)
- [Download previous packaged release v1.0.3](releases/RF-Suite-Blue-v1.0.3.zip)

## Installation

1. Download a ZIP or copy its complete theme folder into the transmitter's `scripts` folder.
2. Restart the transmitter.
3. Open **System > General > Theme**.
4. Select the desired theme.

All themes can remain installed together. `main.luac` is intentionally omitted so ETHOS creates a fresh compiled copy.

## Development

`tools/generate_rf_pro_collection.py` regenerates the nine color variants and their separate release ZIPs from one shared template.
