from email_agent.agent import EmailDraftingAgent
import mlflow
import re


def compose_email(
    bullets: str,
    sender_name: str = "Your Name",
    tone: str = "formal",
    language: str = "en",
) -> dict:
    """
    Entry point for AgentOS: wraps EmailDraftingAgent, prints and logs the composed email.

    Supports multilingual outputs (English and Spanish). Normalizes greetings accordingly.
    """
    agent = EmailDraftingAgent()
    result = agent(
        bullets=bullets, sender_name=sender_name, tone=tone, language=language,
    )

    # Extract subject and email body from the agent's output
    subject = result.get("subject") if isinstance(result, dict) else None
    email_body = result.get("email") if isinstance(result, dict) else None

    # Multilingual greeting normalization
    if email_body:
        if language.lower().startswith("es"):
            # Replace any leading English greeting with Spanish 'Hola'
            email_body = re.sub(
                r"^(?:¡?Hey!?|Hello)\s+([^\n,]+)", r"Hola \1", email_body
            )
        elif language.lower().startswith("en"):
            # Replace any leading Spanish greeting with English 'Hello'
            email_body = re.sub(
                r"^(?:¡?Hey!?|Hola)\s+([^\n,]+)", r"Hello \1", email_body
            )

    # Combine subject and body into full email text
    full_email = f"Subject: {subject}\n\n{email_body}"

    # Print to console for CLI visibility
    print(full_email)

    # Log the email as a plain-text artifact in MLflow
    mlflow.log_text(full_email, "email.txt")

    return result
