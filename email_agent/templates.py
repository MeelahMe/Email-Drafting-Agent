import random
from typing import Dict, List

# Nested: language → tone → section → list of options
TEMPLATES: Dict[str, Dict[str, Dict[str, List[str]]]] = {
    "en": {
        "formal": {
            "greetings": [
                "Dear",
                "Greetings",
                "Good morning",
                "Good afternoon",
                "Good evening",
            ],
            "closings": ["Sincerely", "Kind regards", "Yours faithfully"],
        },
        "friendly": {
            "greetings": ["Hi", "Hello", "Hey there", "Good to hear from you"],
            "closings": ["Cheers", "Thanks", "Talk soon"],
        },
        "concise": {"greetings": ["Hello"], "closings": ["Best", "Regards"],},
    },
    "es": {
        "formal": {
            "greetings": [
                "Estimado",
                "Saludos",
                "Buenos días",
                "Buenas tardes",
                "Buenas noches",
            ],
            "closings": ["Atentamente", "Saludos cordiales", "Cordialmente"],
        },
        "friendly": {
            "greetings": ["Hola", "¡Hey!"],
            "closings": ["¡Gracias!", "Nos vemos"],
        },
        "concise": {"greetings": ["Hola"], "closings": ["Saludos"],},
    },
    # you can add more languages here...
}


def pick_templated(section: str, tone: str, language: str) -> str:
    """
    Pick a random string from TEMPLATES[language][tone][section],
    falling back to English/formal if needed.
    """
    lang_block = TEMPLATES.get(language, TEMPLATES["en"])
    tone_block = lang_block.get(tone, lang_block["formal"])
    items = tone_block.get(section, [])
    if not items:
        # ultimate fallback
        items = TEMPLATES["en"]["formal"][section]
    return random.choice(items)
