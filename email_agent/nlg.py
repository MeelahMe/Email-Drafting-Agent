import re

def rewrite_purpose(purpose: str, language: str = "en") -> str:
    """
    Generate a natural sentence for the email purpose based on a brief phrase.

    - Spanish (es) mappings:
      • Seguimiento: “Quería darle seguimiento a {topic}.”
      • Invitación: “Le escribo para invitarle a {topic}.”
      • Agradecimiento: “Quería agradecerle por {topic}.”
      • Fallback: “Quería informarle sobre {purpose}.”
    - English (en) mappings:
      • Follow-up: “I wanted to follow up on your request.”
      • Project update: “I'm writing to provide an update on the project.”
      • Request: timeline: “I'm reaching out with a request regarding timeline.”
      • Fallback: “I wanted to let you know about {purpose}.”
    """
    p = purpose.strip().rstrip('.')
    lang = language.lower()

    if lang.startswith('es'):
        low = p.lower()
        if re.search(r'\bseguimiento\b', low) or 'follow up' in low:
            topic = re.sub(r'(?i)seguimiento', '', low).strip(': ').strip()
            return f"Quería darle seguimiento a {topic or 'su solicitud'}."
        if re.search(r'invit[ació]n', low):
            topic = re.sub(r'(?i)invit[ació]n', '', low).strip(': ').strip()
            return f"Le escribo para invitarle a {topic}."
        if 'agradecimiento' in low or 'gracias' in low:
            topic = re.sub(r'(?i)(agradecimiento|gracias)', '', low).strip(': ').strip()
            return f"Quería agradecerle por {topic or 'su atención'}."
        return f"Quería informarle sobre {p}."

    # English fallback
    if re.fullmatch(r'(?i)follow[- ]?up', p):
        return "I wanted to follow up on your request."
    if re.fullmatch(r'(?i)project update', p):
        return "I'm writing to provide an update on the project."
    if re.fullmatch(r'(?i)request:?[ \s]*timeline', p):
        return "I'm reaching out with a request regarding timeline."
    return f"I wanted to let you know about {p}."

def rewrite_detail(point: str, language: str = "en") -> str:
    """
    Generate a natural sentence for a detail bullet.

    - Spanish (es) mappings:
      • Completado: “He completado la tarea.”
      • Adjunto: “Por favor, encuentre adjunto {filename}.”
      • Fallback: Capitalize and add period.
    - English (en) mappings:
      • Completed … / Finished … → “I have completed the {rest}.” / “I have finished the {rest}.”
      • Attached … → “Please find the attached {rest}.”
      • Fallback: Append period.
    """
    text = point.strip().rstrip('.')
    lang = language.lower()

    if lang.startswith('es'):
        low = text.lower()
        if low.startswith(('complet', 'finaliz')):
            return f"He {low}."
        if low.startswith('adjunt'):
            m = re.search(r'(?i)adjunt(?:ado)?:?\s*(.*)', text)
            if m and m.group(1):
                return f"Por favor, encuentre adjunto {m.group(1)}."
            return "Por favor, consulte el documento adjunto."
        return text[0].upper() + text[1:] + '.'

    low = text.lower()
    if low.startswith('completed '):
        rest = text[len('Completed '):].strip()
        return f"I have completed the {rest}."
    if low.startswith('finished '):
        rest = text[len('Finished '):].strip()
        return f"I have finished the {rest}."
    if low.startswith('attached '):
        m = re.match(r'(?i)attached\s+(.*)', text)
        if m and m.group(1):
            return f"Please find the attached {m.group(1)}."
    return text + '.'

