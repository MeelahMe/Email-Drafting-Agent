# File: email_agent/agent.py
import re
from datetime import datetime
from email_agent.nlg import rewrite_purpose, rewrite_detail
from .subject_transformer import rewrite_subject_segments

# Keys (other than Changes, Docs update, Deadline) whose list values collapse into sentences
COMPOUND_KEYS = {
    "Milestones", "Dependencies", "Deliverables",
    "Context", "Next steps", "Steps", "Action items",
    "Puntos", "Tareas completadas", "Links", "Risks", "Sample payload"
}

def join_list(items: list[str]) -> str:
    """
    Join a list of items with an Oxford comma and maintain parallel structure.
    """
    cleaned = [item.strip().rstrip('.') for item in items if item]
    n = len(cleaned)
    if n == 0:
        return ""
    if n == 1:
        return cleaned[0]
    if n == 2:
        return f"{cleaned[0]} and {cleaned[1]}"
    return ", ".join(cleaned[:-1]) + f", and {cleaned[-1]}"

def _parse_bullets(bullets: str) -> dict[str, str | list[str]]:
    """
    Parse bullet-point input into a dict mapping keys to values.
    Supports:
      - Top-level bullets (•)
      - List items (-, *, numbered)
      - Multiline fenced code blocks (```…```)
    """
    data: dict[str, str | list[str]] = {}
    current_key: str | None = None
    lines = bullets.splitlines()
    i = 0

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        # Preserve fenced code block as a single string (indented)
        if current_key and stripped.startswith("```"):
            fence = stripped
            block = [lines[i].lstrip()]
            i += 1
            while i < len(lines) and lines[i].strip() != fence:
                block.append(lines[i].lstrip())
                i += 1
            if i < len(lines):
                block.append(lines[i].lstrip())
            # indent block for email readability
            data[current_key] = "\n".join("  " + ln for ln in block)
            i += 1
            continue

        # New top-level bullet defines key
        if stripped.startswith("•"):
            key, _, val = stripped[1:].partition(":")
            current_key = key.strip()
            data[current_key] = val.strip()
        # List items under current key
        elif current_key and (stripped.startswith(("-", "*")) or re.match(r"\d+\.", stripped)):
            item = re.sub(r"^[\-\*\d\.\s]+", "", stripped).strip()
            prev = data[current_key]
            if isinstance(prev, list):
                prev.append(item)
            else:
                data[current_key] = [prev, item] if prev else [item]
        # Continuation lines (append to last item or value)
        elif current_key:
            prev = data[current_key]
            if isinstance(prev, list):
                prev[-1] = f"{prev[-1]} {stripped}"
            else:
                data[current_key] = f"{prev} {stripped}"
        i += 1

    return data

def _make_greeting(recipient: str, language: str) -> str:
    """
    Produce a time-based greeting with recipient name(s).
    """
    names = [part.strip().split(",", 1)[0]
             for part in re.split(r"[;,]", recipient)
             if part.strip()]
    hour = datetime.now().hour
    if language.lower().startswith("es"):
        sal = "Buenos días" if hour < 12 else "Buenas tardes" if hour < 18 else "Buenas noches"
    else:
        sal = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
    return f"{sal}, {join_list(names)}," if names else f"{sal},"

def _rewrite_purpose_full(purpose: str, tone: str, language: str) -> str:
    """
    Create a polished purpose sentence, handling alerts and share/attach.
    """
    p = purpose.strip().rstrip(".")
    low = p.lower()
    if tone.lower() == "urgent":
        m = re.match(r"(?i)alert(?:\s+and)?\s+(.+)", p)
        if m:
            return f"I'm sending an alert to {m.group(1)}."
    if language.lower().startswith("en") and low.startswith("share "):
        m = re.match(r"(?i)share\s+(.+?)\s+and\s+attach\s+(.+)", p)
        if m:
            return f"I'm sharing our {m.group(1).lower()} and attaching the {m.group(2)}."
    return rewrite_purpose(p, language)

def _select_closing(tone: str, language: str, sender: str) -> str:
    """
    Choose a closing phrase based on tone and language.
    """
    lang = language.lower()
    tone_key = tone.lower()
    if lang.startswith("es"):
        closing = {"friendly": "Saludos", "urgent": "Gracias por su pronta atención"}.get(tone_key, "Cordialmente")
    else:
        closing = {"friendly": "Best regards", "urgent": "Thank you for your immediate attention"}.get(tone_key, "Sincerely")
    return f"{closing},\n{sender}"

class EmailDraftingAgent:
    def __call__(
        self,
        bullets: str,
        sender_name: str = "Your Name",
        tone: str = "formal",
        language: str = "en"
    ) -> dict:
        """
        Compose an email from bullet-point input.
        """
        data = _parse_bullets(bullets)

        # Build subject
        raw = data.get("Purpose", "").strip().rstrip(".") or "Update"
        subject = rewrite_subject_segments(raw)
        if tone.lower() == "urgent":
            subject = f"URGENT: {subject}"

        # Greeting
        greeting = _make_greeting(data.get("Recipient") or data.get("Recipients", ""), language)

        # Body
        body: list[str] = []
        if (purpose := data.get("Purpose", "")).strip():
            body.append(_rewrite_purpose_full(purpose, tone, language))

        for key, val in data.items():
            if key in {"Recipient", "Recipients", "Purpose", "Attachment", "Attached"}:
                continue
            # Skip empty
            if isinstance(val, str) and not val.strip():
                continue
            if isinstance(val, list) and not val:
                continue

            if key == "Changes":
                # Expand Changes into a bulleted list
                items = val if isinstance(val, list) else [v.strip() for v in str(val).split(",")]
                body.append("Changes:")
                for item in items:
                    text = item.rstrip(".")
                    text = re.sub(r"\b1000\b", "1,000", text)
                    text = text[0].upper() + text[1:] + "."
                    body.append(f"- {text}")

            elif key.lower() == "docs update":
                # Render Docs update as a sentence
                body.append(rewrite_detail(val, language))

            elif key.lower() == "deadline":
                # Render Deadline as a sentence
                dl = val.strip().rstrip(".")
                body.append(f"Deadline: {dl}.")

            elif key in COMPOUND_KEYS:
                items = val if isinstance(val, list) else [v.strip() for v in str(val).split(",")]
                body.append(f"{key}: {join_list(items)}.")

            elif isinstance(val, str) and val.lstrip().startswith("```"):
                # Preserve fenced code block
                body.append(val)

            elif isinstance(val, str) and val.strip().startswith("{") and val.strip().endswith("}"):
                # Preserve inline JSON
                body.append(val)

            elif isinstance(val, list):
                for item in val:
                    body.append(rewrite_detail(item, language))

            elif key.lower() == "next steps":
                step = val.strip().rstrip(".")
                body.append(f"Next steps: {step}.")

            else:
                body.append(rewrite_detail(val, language))

        # Attachment
        attach = data.get("Attachment") or data.get("Attached")
        if attach:
            body.append(f"Please find the attached {attach}.")

        # Closing
        closing = _select_closing(tone, language, sender_name)
        email_body = "\n\n".join([greeting] + body + [closing])

        return {"subject": subject, "email": email_body}
