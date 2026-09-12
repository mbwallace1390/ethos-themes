"""Refresh every catalog image from theme sources, without regenerating art."""
from generate_readme_previews import FAMILIES
from generate_custom_art_themes import COLLECTIONS
from generate_cancer_awareness_themes import THEMES as AWARENESS
from generate_rf_pro_preview import THEMES as RF_PRO
from generate_america250_theme import preview as america_preview
from preview_lib import render_collection


def main():
    america_preview()
    for slug, (title, themes) in FAMILIES.items():
        render_collection(slug, title, themes)
    for slug, (title, themes) in COLLECTIONS.items():
        render_collection(slug, title, themes)
    render_collection("cancer-awareness", "Cancer Awareness", [t[0] for t in AWARENESS])
    render_collection("rf-pro", "RF Pro Color Collection", RF_PRO)
    render_collection("classic", "RF Suite Blue", ["rfsuite-blue"])
    print("Generated all 17 catalog previews from current theme sources")


if __name__ == "__main__":
    main()
