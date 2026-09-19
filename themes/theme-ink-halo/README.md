# Ink & Halo v1.0.2

Requires ETHOS 26.1.0 or newer; API checked against 26.1.2. Radio validation is still required.

Install the ZIP with ETHOS Suite's local ZIP installer. For manual ZIP installation, create `scripts/theme-ink-halo/` on the transmitter and extract the ZIP contents into that folder.

**Collection:** Signature

A standalone FrSky ETHOS theme.

- Focus: `outline`
- Controls: rounded
- Internal key: `INKHALO`
- Automatically selects 784x50 artwork on 800px radios and 464x50 artwork on standard X18 radios
- Original halo artwork, drawn at each native display width
- Glow is baked into opaque PNGs; no animation or background drawing
- Soft-white and pale-blue ETHOS wordmark baked into the header artwork
- Raised halo arc and a clear area around the wordmark at both display sizes
- Transparent logo override prevents the default green logo overlapping it
- Startup and About logos are unchanged; ETHOS 26 exposes no documented theme option for them

To install from repository sources, copy `theme-ink-halo` into the transmitter `scripts` folder, restart, and select **Ink & Halo** under **System > General > Theme**.
