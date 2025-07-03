import re
from datetime import datetime
from email_agent.nlg import rewrite_purpose, rewrite_detail

# Keys whose list values should be collapsed into a single sentence
COMPOUND_KEYS = {
    "Changes", "Milestones", "Dependencies", "Deliverables",
    "Context", "Next steps", "Steps", "Action items", "Puntos",
    "Tareas completadas", "Links", "Risks", "Sample payload"
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


def _parse_bullets(bullets: str) -> dict:
    """
    Parse bullet-point input into a dict of key → value or list of values.
    Supports top-level bullets (•), dash/list items (- or *), and numbered lists.
    """
    data: dict[str, str | list[str]] = {}
    current_key: str | None = None

    for line in bullets.splitlines():
        stripped = line.strip()
        if stripped.startswith("•"):
            key, _, val = stripped[1:].partition(":")
            current_key = key.strip()
            data[current_key] = val.strip()
        elif current_key and (stripped.startswith(("-", "*")) or re.match(r"\d+\.", stripped)):
            # List item under current_key
            item = re.sub(r"^[\-\*\d\.\s]+", "", stripped).strip()
            prev = data[current_key]
            if isinstance(prev, list):
                prev.append(item)
            else:
                data[current_key] = [prev, item] if prev else [item]
        elif current_key:
            # Continuation of previous value or last list item
            prev = data[current_key]
            if isinstance(prev, list):
                prev[-1] = f"{prev[-1]} {stripped}"
            else:
                data[current_key] = f"{prev} {stripped}"
    return data


def _rewrite_subject(purpose: str, tone: str, language: str) -> str:
    """
    Build a title-case subject, prefixing with 'URGENT:' if needed,
    converting 'Share X and attach Y' → 'X & Y', defaulting to 'Update'.
    """
    p = purpose.strip().rstrip(".")
    if not p:
        base = "Update"
    else:
        share_match = re.match(r"(?i)share\s+(.+?)\s+and\s+attach\s+(.+)", p)
        if share_match:
            core = f"{share_match.group(1)} & {share_match.group(2)}".title()
            base = core
        else:
            base = p.title()

    if tone.lower() == "urgent":
        return f"URGENT: {base}"
    return base


def _make_greeting(recipient: str, language: str) -> str:
    """
    Produce a time-based greeting.
    Drops roles after commas, joins multiple names with 'and',
    and ends with a comma.
    """
    # Extract just the names (drop roles)
    names = [part.strip().split(",", 1)[0]
             for part in re.split(r"[;,]", recipient)
             if part.strip()]
    greeting_time = datetime.now().hour
    if language.lower().startswith("es"):
        salutation = (
            "Buenos días" if greeting_time < 12
            else "Buenas tardes" if greeting_time < 18
            else "Buenas noches"
        )
    else:
        salutation = (
            "Good morning" if greeting_time < 12
            else "Good afternoon" if greeting_time < 18
            else "Good evening"
        )

    if not names:
        return f"{salutation},"
    return f"{salutation}, {join_list(names)},"


def _rewrite_purpose_full(purpose: str, tone: str, language: str) -> str:
    """
    Create a polished purpose sentence.
    Special-cases urgent alerts and share/attach patterns,
    otherwise delegates to rewrite_purpose().
    """
    p = purpose.strip().rstrip(".")
    low = p.lower()

    if tone.lower() == "urgent":
        alert_match = re.match(r"(?i)alert(?:\s+and)?\s+(.+)", p)
        if alert_match:
            return f"I'm sending an alert to {alert_match.group(1)}."

    if language.lower().startswith("en") and low.startswith("share "):
        share_match = re.match(r"(?i)share\s+(.+?)\s+and\s+attach\s+(.+)", p)
        if share_match:
            findings = share_match.group(1).strip()
            attach = share_match.group(2).strip()
            return f"I'm sharing our {findings.lower()} and attaching the {attach}."

    return rewrite_purpose(p, language)


def _select_closing(tone: str, language: str, sender: str) -> str:
    """
    Choose a closing phrase based on tone and language, ending with sender.
    """
    lang = language.lower()
    tone_key = tone.lower()
    if lang.startswith("es"):
        closing = {
            "friendly": "Saludos",
            "urgent": "Gracias por su pronta atención"
        }.get(tone_key, "Cordialmente")
    else:
        closing = {
            "friendly": "Best regards",
            "urgent": "Thank you for your immediate attention"
        }.get(tone_key, "Sincerely")
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
        Compose an email from bullet-point input, enforcing:
         - Oxford commas
         - Title case subjects
         - Parallelism in lists
         - Proper punctuation and salutation style
        """
        data = _parse_bullets(bullets)
        subject = _rewrite_subject(data.get("Purpose", ""), tone, language)
        greeting = _make_greeting(
            data.get("Recipient") or data.get("Recipients", ""),
            language
        )

        body: list[str] = []
        # Purpose
        if data.get("Purpose", "").strip():
            body.append(_rewrite_purpose_full(
                data["Purpose"], tone, language))

        # Other bullets
        for key, val in data.items():
            if key in {"Recipient", "Recipients", "Purpose", "Attachment", "Attached"}:
                continue

            # Collapse compound lists
            if key in COMPOUND_KEYS:
                items = val if isinstance(val, list) else [v.strip() for v in val.split(",")]
                sentence = f"{key}: {join_list(items)}."
                body.append(sentence)

            # JSON or code payloads
            elif isinstance(val, str) and val.strip().startswith("{") and val.strip().endswith("}"):
                body.append(val.strip())

            # Regular lists
            elif isinstance(val, list):
                for item in val:
                    body.append(rewrite_detail(item, language))

            # Single strings
            else:
                if key.lower() == "next steps":
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

