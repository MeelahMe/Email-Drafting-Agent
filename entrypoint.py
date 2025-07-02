from email_agent.agent import EmailDraftingAgent
import mlflow

def compose_email(
    bullets: str,
    sender_name: str = "Your Name",
    tone: str = "formal",
    language: str = "en",
) -> dict:
    """
    Entry point for AgentOS: wraps EmailDraftingAgent and logs the composed email.
    Prints the formatted email to stdout and saves it as a text artifact.
    """
    agent = EmailDraftingAgent()
    result = agent(
        bullets=bullets,
        sender_name=sender_name,
        tone=tone,
        language=language,
    )

    # Extract the subject and email body from the result
    subject = result.get("subject") if isinstance(result, dict) else None
    email_body = result.get("email") if isinstance(result, dict) else None

    # Combine into a single formatted string
    full_email = f"Subject: {subject}\n\n{email_body}"

    # Print the email to the console
    print(full_email)

    # Log the email as a plain-text artifact
    mlflow.log_text(full_email, "email.txt")

    return result

