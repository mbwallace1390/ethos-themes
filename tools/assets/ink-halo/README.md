# Ink & Halo header wordmark

`ethos-wordmark.png` is a 1000x204 RGBA PNG with genuine transparency, including
the letter interiors. Its ETH letters are soft white (#F4F7FC), and OS is pale
blue (#BDD7FF). It preserves the original letter geometry and edge alpha from
[FrSky's official logo in the 26.1 manual](https://github.com/FrSkyRC/ethos-manual/blob/26.1/french/assets/ethos-logo-reversed.png).
The tagline and small trademark were omitted for readability at header size.

The ETHOS wordmark belongs to FrSky. This recolored adaptation is for the
unofficial Ink & Halo theme and does not imply endorsement by FrSky.

The user approved direct image processing after image-editor attempts produced
painted checkerboards or damaged edges. The accepted asset was produced from
the original transparent logo, preserving its alpha and assigning the two
theme colors to the letters. Generated alternatives were not used.

`tools/generate_ink_halo_theme.py` downsizes this asset to 128x26 and composites
it with its alpha over each native toolbar. The finished toolbar remains an
opaque PNG. This source asset is not installed on the radio; no extra runtime
bitmap, rendering loop, or task is added. Regeneration uses the checked-in
asset directly and does not require an image service or network access.
