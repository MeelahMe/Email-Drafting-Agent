import re

# Updated rule-based rewrite library with more patterns

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
        raw_topic = re.sub(r"update", "", p, flags=re.IGNORECASE).strip()
        topic = raw_topic.lower() if raw_topic else "project"
        return f"I'm writing to provide an update on the {topic}."
    # thank you case
    if "thank" in low:
        raw = re.sub(r"thank( you)?", "", p, flags=re.IGNORECASE).strip()
        if raw:
            return f"I wanted to thank you for {raw}."
        return "I wanted to thank you."
    # invitation case
    if "invitation" in low:
        raw_topic = re.sub(r"invitation", "", p, flags=re.IGNORECASE).strip()
        topic = raw_topic if raw_topic else "event"
        return f"I'm writing to invite you to {topic}."
    # status update case
    if "status update" in low or "status" in low:
        return "I'm writing to provide a status update."
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
    # colon-based fields
    if ":" in text:
        label, value = text.split(":", 1)
        label_l = label.strip().lower()
        value = value.strip()
        if label_l == "venue":
            return f"The venue is {value}."
        if label_l == "rsvp":
            return f"Please RSVP by {value}."
        if label_l == "cc":
            return f"I've CC'd {value} for visibility."
        if label_l == "next steps":
            return f"Next steps: {value}."
    # past-tense verbs → present perfect with 'the'
    if low.startswith(("completed", "finished", "sent")):
        parts = low.split(" ", 1)
        if len(parts) > 1:
            verb, obj = parts[0], parts[1]
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
    return text[0].upper() + text[1:] + "."

