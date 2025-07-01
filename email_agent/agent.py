# email_agent/agent.py

from typing import Dict, List
from email_agent.parser import parse_bullets
from email_agent.templates import pick, GREETINGS, CLOSINGS
from email_agent.nlg import rewrite_purpose, rewrite_detail

class EmailDraftingAgent:
    """
    Agent that transforms bullet inputs into a polished, professional email draft.
    """
    def __call__(self, bullets: str, sender_name: str = "Your Name") -> Dict[str, str]:
        # Parse the raw bullet input
        data = parse_bullets(bullets)
        subject = data["purpose"].capitalize() if data["purpose"] else "No Subject"

        # Greeting
        recipient = data["recipient"] or "there"
        greeting = f"{pick(GREETINGS)} {recipient},"

        # Body construction using rule-based NLG helpers
        body_parts: List[str] = []
        if data["purpose"]:
            body_parts.append(rewrite_purpose(data["purpose"]))
        for pt in data["points"]:
            body_parts.append(rewrite_detail(pt))
        body = " ".join(body_parts)

        # Closing
        closing = f"{pick(CLOSINGS)},\n{sender_name}"

        # Assemble full email
        email_text = f"{greeting}\n\n{body}\n\n{closing}"
        return {"subject": subject, "email": email_text}

