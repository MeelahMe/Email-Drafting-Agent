from email_agent.agent import EmailDraftingAgent


def test_basic():
    bullets = """\
• Recipient: Taylor
• Purpose: Follow-up on assignment
• Completed the task and attached it
• Offer to clarify anything"""
    out = EmailDraftingAgent()(bullets=bullets)
    assert "Taylor" in out["email"]
    assert out["subject"].startswith("Follow-up")
