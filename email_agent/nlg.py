import re

def rewrite_purpose(purpose: str, language: str = "en") -> str:
    p = purpose.strip().rstrip(".")
    low = p.lower()

    if language == "es":
        # Seguimiento
        if "seguimiento" in low or "follow up" in low:
            topic = re.sub(r"seguimiento", "", low).strip() or "su solicitud"
            return f"Quería darle seguimiento a {topic}."
        # Invitación
        if "invitación" in low or "invitacion" in low:
            topic = re.sub(r"invit[ació]n", "", low, flags=re.IGNORECASE).strip() or "evento"
            return f"Le escribo para invitarle a {topic}."
        # Agradecimiento
        if "gracias" in low or "agradecimiento" in low:
            return f"Quería agradecerle por {low.replace('agradecimiento','').strip()}."
        # Default
        return f"Quería informarle sobre {p}."

    # FALLBACK to English (existing logic)...

def rewrite_detail(point: str, language: str = "en") -> str:
    text = point.strip().rstrip(".")
    low = text.lower()

    if language == "es":
        # Completé la tarea
        if low.startswith("complet") or low.startswith("finaliz"):
            return f"He {low}."
        # Adjunto
        if low.startswith("adjunt"):
            m = re.search(r"adjunt(?:ado)?:?\s*(.*)", text, re.IGNORECASE)
            if m and m.group(1):
                return f"Por favor, encuentre adjunto {m.group(1).strip()}."
            return "Por favor, consulte el documento adjunto."
        # Default Spanish fallback: capitalize + period
        return text[0].upper() + text[1:] + "."

    # FALLBACK to English (existing logic)...

