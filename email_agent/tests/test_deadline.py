import pytest
from email_agent.agent import EmailDraftingAgent

def test_deadline_format():
    bullets = """\
• Recipient: Jane
• Purpose: Sync
• Deadline: EOD Friday (UTC−07:00)
"""
    out = EmailDraftingAgent()(bullets=bullets)
    # The body should include a properly punctuated Deadline line
    assert "Deadline: EOD Friday (UTC−07:00)." in out["email"]

