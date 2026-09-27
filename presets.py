"""Har creator type ka editing style. Phase 1 mein sirf 'talking' active hai."""

PRESETS = {
    "talking": {
        "label": "Talking / Vlog",
        "min_sec": 20,
        "max_sec": 60,
        "ai_hint": (
            "Pick moments with a strong hook in the first 3 seconds: a bold opinion, "
            "a funny line, a surprising fact, a story payoff or an emotional reaction. "
            "Each clip must make sense on its own without extra context."
        ),
        "caption_style": "FontName=Arial,FontSize=14,Bold=1,PrimaryColour=&H00FFFFFF,"
                         "OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=0,"
                         "Alignment=2,MarginV=90",
    },
    # Phase 5 mein add honge: food, travel, gaming, podcast
}
