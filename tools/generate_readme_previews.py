"""Generate the standalone-family previews from current theme sources."""
from preview_lib import parse_theme, render_collection

FAMILIES = {
    "retro-instrument": (
        "Retro Instrument",
        ["amber-instrument", "phosphor-green", "ice-instrument"],
    ),
    "soft": (
        "Soft",
        ["soft-lavender", "soft-mint", "soft-coral", "soft-sky"],
    ),
    "oled-stealth": (
        "OLED Stealth",
        ["oled-blue", "oled-red", "oled-green", "oled-white"],
    ),
    "daylight": (
        "Daylight",
        ["daylight-blue", "daylight-orange", "daylight-green"],
    ),
    "industrial": (
        "Industrial",
        ["carbon", "gunmetal", "hazard", "titanium"],
    ),
    "two-tone": (
        "Two-Tone",
        ["violet-circuit", "blue-vector", "ember-signal", "neon-fusion"],
    ),
    "molten": (
        "Molten",
        ["molten-ember", "molten-sulfur", "molten-verdigris"],
    ),
    "elements": (
        "Elements",
        ["summit", "aurora", "abyss", "prism"],
    ),
    "texture": (
        "Texture",
        ["loom", "mosaic", "halftone", "bloom"],
    ),
}


def generate_family(slug, title, theme_slugs):
    render_collection(slug, title, theme_slugs)


if __name__ == "__main__":
    for slug, (title, theme_slugs) in FAMILIES.items():
        generate_family(slug, title, theme_slugs)
    print(f"Generated {len(FAMILIES)} standalone-family previews")
