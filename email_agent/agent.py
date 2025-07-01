from typing import Dict
from email_agent.parser import parse_bullets
from email_agent.templates import pick, GREETINGS, CLOSINGS

class EmailDraftingAgent:
    """
    Agent that transforms bullet-point input into a polished email draft.
    """

    def __call__(self, bullets: str, sender_name: str = "Your Name") -> Dict[str, str]:
        """
        Builds an email subject and body based on input bullets.

        Args:
            bullets: Multiline string of bullet-point inputs.
            sender_name: Name of the email sender to use in the closing.

        Returns:
            Dict with 'subject' and 'email' keys.
        """
        data = parse_bullets(bullets)

        # Determine subject
        subject = data["purpose"].capitalize() if data["purpose"] else "Following up"

        # Build greeting
        recipient = data["recipient"].split()[0] if data["recipient"] else "there"
        greeting = f"{pick(GREETINGS)} {recipient},"

        # Build body
        body_sections = []
        if data["purpose"]:
            body_sections.append(f"{data['purpose'].capitalize()}.")
        for point in data["points"]:
            body_sections.append(f"- {point}.")
        body = "\n".join(body_sections)

        # Build closing
        closing = f"{pick(CLOSINGS)},\n{sender_name}"

        # Assemble email with consistent spacing
        parts = [greeting]
        if body:
            parts.append(body)
        parts.append(closing)
        email_text = "\n\n".join(parts)

        return {"subject": subject, "email": email_text}
