"""Generate Pro collection previews from current theme sources."""
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

DISPLAY_NAMES = {
    "rfblue-pro": "Blue Pro",
    **{f"rf-{color}-pro": f"{color.title()} Pro" for color in (
        "violet", "emerald", "ember", "magenta", "cyan",
        "crimson", "gold", "teal", "lime",
    )},
}


def main():
    render_collection("rf-pro", "Pro Color Collection", THEMES, display_names=DISPLAY_NAMES)


if __name__ == "__main__":
    main()
