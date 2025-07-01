from .parser import parse_bullets
from .templates import pick, GREETINGS, CLOSINGS

class EmailDraftingAgent:
    """
    AgentOS will instantiate this and call __call__(bullets=str) → dict
    """

    def __call__(self, bullets: str) -> dict:
        data = parse_bullets(bullets)

        recipient_name = data["recipient"] or "there"
        greeting = f"{pick(GREETINGS)} {recipient_name.split()[0]},"

        # Body
        body_lines = []
        if data["purpose"]:
            body_lines.append(f"{data['purpose'].capitalize()}.")
        body_lines.extend(f"- {pt}." for pt in data["points"])

        closing = f"{pick(CLOSINGS)},\nYour Name"

        email_text = "\n\n".join([greeting, "\n".join(body_lines), closing])
        subject = data["purpose"].capitalize() if data["purpose"] else "Following up"

        return {"subject": subject, "email": email_text}

