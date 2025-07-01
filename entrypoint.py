from email_agent.agent import EmailDraftingAgent
import json

def compose_email(bullets: str, sender_name: str = "Your Name") -> dict:
    agent = EmailDraftingAgent()
    result = agent(bullets=bullets, sender_name=sender_name)
    # Pretty-print to console:
    print(json.dumps(result, indent=2))
    return result

