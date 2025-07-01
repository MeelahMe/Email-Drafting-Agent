from email_agent.agent import EmailDraftingAgent

def generate_email(bullets: str, sender_name: str = "Your Name") -> dict:
    agent = EmailDraftingAgent()
    return agent(bullets=bullets, sender_name=sender_name)

