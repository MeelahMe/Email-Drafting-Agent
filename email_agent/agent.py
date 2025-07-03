from typing import Dict, List
from email_agent.parser import parse_bullets
from email_agent.templates import pick_templated
from email_agent.nlg import rewrite_purpose, rewrite_detail

class EmailDraftingAgent:
    """
    Agent that transforms bullet inputs into a polished, multilingual, multi-tone email draft.
    """
    def __call__(
        self,
        bullets: str,
        sender_name: str = "Your Name",
        tone: str = "formal",
        language: str = "en",
    ) -> Dict[str, str]:
        # Parse the raw bullet input (pass language for multilingual support)
        try:
            data = parse_bullets(bullets, language=language)
        except TypeError:
            data = parse_bullets(bullets)

        subject = data.get("purpose", "").capitalize() if data.get("purpose") else "No Subject"

        # Greeting
        recipient = data.get("recipient", "there") or "there"
        greeting = f"{pick_templated('greetings', tone, language)} {recipient},"

        # Body construction using NLG helpers
        body_parts: List[str] = []
        if data.get("purpose"):
            body_parts.append(rewrite_purpose(data["purpose"], language))
        for pt in data.get("points", []):
            body_parts.append(rewrite_detail(pt, language))
        body = " ".join(body_parts)

        # Closing
        closing = f"{pick_templated('closings', tone, language)},\n{sender_name}"

        # Assemble full email
        email_text = f"{greeting}\n\n{body}\n\n{closing}"
        return {"subject": subject, "email": email_text}

