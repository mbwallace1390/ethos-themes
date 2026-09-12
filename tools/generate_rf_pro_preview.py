"""Generate RF Pro previews from current theme sources."""
from preview_lib import render_collection

THEMES = [
    "rfblue-pro",
    "rf-violet-pro",
    "rf-emerald-pro",
    "rf-ember-pro",
    "rf-magenta-pro",
    "rf-cyan-pro",
    "rf-crimson-pro",
    "rf-gold-pro",
    "rf-teal-pro",
    "rf-lime-pro",
]


def main():
    render_collection("rf-pro", "RF Pro Color Collection", THEMES)


if __name__ == "__main__":
    main()
