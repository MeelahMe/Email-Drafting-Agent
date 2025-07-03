import re
import pytest
from entrypoint import compose_email

# Dummy agent to avoid external dependencies
class DummyAgent:
    def __call__(self, bullets, sender_name, tone, language):
        # Simulate output from EmailDraftingAgent
        subject = "Test Subject"
        # Base email uses English greeting by default
        email = f"Hey John,\n\nThis is a test body.\n\nThanks,\n{sender_name}"
        return {"subject": subject, "email": email}

@pytest.fixture(autouse=True)
def patch_agent_and_mlflow(monkeypatch):
    # Patch the EmailDraftingAgent to use DummyAgent
    import entrypoint
    monkeypatch.setattr(entrypoint, 'EmailDraftingAgent', lambda: DummyAgent())
    # Patch mlflow.log_text to a no-op
    monkeypatch.setattr(entrypoint.mlflow, 'log_text', lambda text, name: None)

def test_spanish_greeting_normalization(capsys):
    bullets = '• Recipient: John\n• Purpose: Test\n• Completed the task'
    compose_email(bullets, sender_name="Ana", tone="friendly", language="es")
    output = capsys.readouterr().out
    # Expect subject and Spanish greeting
    assert output.startswith("Subject: Test Subject"), "Subject line missing or incorrect."
    # Check that greeting was normalized to Hola
    assert re.search(r"\n\nHola John," , output), f"Spanish greeting not normalized: {output}"

def test_english_greeting_normalization(capsys):
    bullets = '• Recipient: John\n• Purpose: Test\n• Completed the task'
    compose_email(bullets, sender_name="Ana", tone="friendly", language="en")
    output = capsys.readouterr().out
    # Expect subject and English greeting
    assert output.startswith("Subject: Test Subject"), "Subject line missing or incorrect."
    # Check that greeting was normalized to Hello
    assert re.search(r"\n\nHello John," , output), f"English greeting not normalized: {output}"

def test_full_email_format(capsys):
    bullets = '• Recipient: John\n• Purpose: Test\n• Completed the task'
    result = compose_email(bullets, sender_name="Ana", tone="formal", language="en")
    # The function returns the original result dict
    assert isinstance(result, dict)
    assert result.get('subject') == "Test Subject"
    assert 'Test Subject' in result.get('subject')
    # Email field should be present in returned dict
    assert 'email' in result
    # Output printed should include body text
    printed = capsys.readouterr().out
    assert "This is a test body." in printed, "Email body missing in printed output."

