# RF Suite Blue v1.0.5

A dark FrSky ETHOS theme that replaces the yellow selected-control highlight with blue, including selected controls inside Rotorflight RF Suite.

## Changes in v1.0.5

- Uses a thinner, sharper 784x50 toolbar gradient.
- Changes the outer page background to blue-black so ETHOS's fixed side margins blend into the theme instead of appearing gray.
- Keeps the proven six-character internal theme key `RFBlue`.
- Keeps the 784-pixel toolbar width because testing confirmed ETHOS enforces that toolbar safe area even when an 800-pixel image is supplied.
- Omits `main.luac` so ETHOS compiles a fresh copy during startup.

## Installation

1. Delete any existing `scripts/theme-rfsuite-blue` folder.
2. Restart the transmitter.
3. Install the release ZIP through ETHOS Suite, or copy the included `theme-rfsuite-blue` folder into `scripts`.
4. Restart the transmitter again.
5. Select **RF Suite Blue** under **System > General > Theme**.

- Automatically selects 784x50 artwork on 800px radios and 464x50 artwork on standard X18 radios
