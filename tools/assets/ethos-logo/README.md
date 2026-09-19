# Shared ETHOS wordmark mask

`wordmark-alpha.png` contains only the original 1000x204 edge/transparency mask
from the approved `../ink-halo/ethos-wordmark.png` asset. That asset preserves
the letter geometry from [FrSky's official logo in the 26.1 manual](https://github.com/FrSkyRC/ethos-manual/blob/26.1/french/assets/ethos-logo-reversed.png),
with its tagline and small trademark omitted for readability at radio-header size.
The mask is an 8-bit grayscale PNG: white is opaque, black is transparent.
It is a build input, not an image installed on the radio.

The user approved direct image processing for these theme adaptations. The mask
was extracted with Pillow's `getchannel("A")`; no letter geometry was redrawn.
The ETHOS wordmark belongs to FrSky. These unofficial theme adaptations do not
imply endorsement by FrSky.

`theme_lib.add_toolbar_logo` produces a 128x26 RGBA PNG for each ordinary theme.
It uses the final palette's primary text color for ETH and highlight color for
OS, plus a thin outline selected from that palette for contrast over patterned
artwork. The original proportions and transparent letter interiors are retained.
All processing happens on the desktop; the radio loads one static bitmap during
initialization. Generation needs no network access or external font.

America 250 and Ink & Halo keep their existing transparent 1x1 overrides. Their
toolbar designs already provide their own centered inscription or wordmark.
