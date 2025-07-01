import re

def rewrite_purpose(purpose: str) -> str:
    """
    Turns a raw purpose string into a proper opening sentence.
    """
    p = purpose.strip().rstrip('.')
    low = p.lower()
    # follow-up case
    if "follow-up" in low or "follow up" in low:
        topic = re.sub(r"follow[- ]?up", "", low).strip() or "your request"
        return f"I wanted to follow up on {topic}."
    # update case
    if "update" in low:
        # extract topic before 'update'
        raw_topic = re.sub(r"update", "", p, flags=re.IGNORECASE).strip()
        topic = raw_topic.lower() if raw_topic else "project"
        return f"I'm writing to provide an update on the {topic}."
    # request case
    if "request" in low:
        if ":" in p:
            topic = p.split(":", 1)[1].strip().lower()
        else:
            topic = re.sub(r"request", "", p, flags=re.IGNORECASE).strip().lower()
        return f"I'm reaching out with a request regarding {topic}."
    # default
    return f"I wanted to let you know about {p}."


def rewrite_detail(point: str) -> str:
    """
    Turns a raw detail bullet into a clean sentence.
    """
    text = point.strip().rstrip('.')
    low = text.lower()
    # past-tense verbs → present perfect with 'the'
    if low.startswith(("completed", "finished", "sent")):
        parts = low.split(" ", 1)
        if len(parts) > 1:
            verb = parts[0]
            obj = parts[1]
            return f"I have {verb} the {obj}."
        return f"I have {low}."
    # attachment detection
    if low.startswith(("attach", "attached")):
        m = re.search(r"attach(?:ed)?:? *(.*)", text, re.IGNORECASE)
        if m and m.group(1):
            return f"Please find the attached {m.group(1).strip()}."
        return "Please see the attached document."
    # fallback: capitalize first letter and add period
    return text[0].upper() + text[1:] + "."

