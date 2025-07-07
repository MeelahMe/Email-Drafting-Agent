# File: email_agent/tests/test_agent_rigorous.py
import re
import pytest
from email_agent.agent import EmailDraftingAgent, _parse_bullets, join_list
from email_agent.subject_transformer import rewrite_subject_segments
from email_agent.nlg import rewrite_purpose, rewrite_detail

@pytest.fixture
def agent():
    return EmailDraftingAgent()

def test_empty_bullets_defaults(agent):
    out = agent(bullets="", sender_name="X", tone="formal", language="en")
    # Subject defaults to "Update"
    assert out["subject"] == "Update"
    # Body still has greeting + default closing
    assert "Good " in out["email"]
    assert out["email"].endswith("X")

def test_urgent_tone_prefix_and_closing(agent):
    bullets = "• Purpose: Alert server down"
    out = agent(bullets=bullets, sender_name="Ops", tone="urgent", language="en")
    assert out["subject"].startswith("URGENT:")
    assert "Thank you for your immediate attention" in out["email"]

def test_spanish_multilingual_and_join_list():
    # join_list Oxford comma
    assert join_list(["uno", "dos", "tres"]) == "uno, dos, and tres"
    # rewrite purpose in Spanish fallback
    res = rewrite_purpose("Nuevo lanzamiento", language="es")
    assert res.startswith("Quería informarle sobre Nuevo lanzamiento")

def test_subject_transformer_acronyms_and_and():
    inp = "review API and CPU benchmarks"
    out = rewrite_subject_segments(inp)
    # Hits both acronym preservation and ampersand
    assert out == "Review API & CPU Benchmarks"

def test_code_block_passthrough_and_json_payload(agent):
    bullets = """\
• Purpose: Share configs
• Sample payload (JSON):
  ```json
  {"key": "value", "list":[1,2,3]}
  ```"""
    out = agent(bullets=bullets)
    # JSON fence should appear verbatim
    email_body = out["email"]
    assert "```json" in email_body
    assert '"list":[1,2,3]' in email_body

@pytest.mark.parametrize("detail,expected", [
    ("completed task", "I have completed the task."),
    ("Finished report", "I have finished the report."),
    ("attached file.txt", "Please find the attached file.txt."),
    ("see `docs/x.md` for full spec", "See `docs/x.md` for full spec."),
])
def test_rewrite_detail_english(detail, expected):
    assert rewrite_detail(detail, language="en") == expected

def test_parse_bullets_continuation_and_numbering():
    raw = """\
• Key: First line
  continues here
  1. Item one
  2. Item two"""
    data = _parse_bullets(raw)
    assert isinstance(data["Key"], list)
    # ensure continuation merged into first element
    assert "continues here" in data["Key"][0]
    assert data["Key"][1] == "Item one"

def test_multiple_recipients_and_greeting(agent):
    bullets = "• Recipients: Alice; Bob, Charlie\n• Purpose: Follow-up"
    out = agent(bullets=bullets)
    # Greeting lists all names
    assert "Alice and Bob and Charlie" in out["email"] or re.search(r"Alice, Bob, and Charlie", out["email"])

def test_deadline_and_docs_update_separate_sentences(agent):
    bullets = """\
• Purpose: Update docs
• Docs update: see `docs/a.md` for full spec
• Deadline: 2025-12-31"""
    out = agent(bullets=bullets)
    body = out["email"]
    # Docs update appears as standalone sentence ending with period
    assert "See `docs/a.md` for full spec." in body
    # Deadline is its own sentence
    assert "Deadline: 2025-12-31." in body

def test_no_recipient_or_purpose(agent):
    # Ensure missing Recipient/Purpose don't crash or add stray keys
    bullets = "• Changes:\n  - One\n  - Two"
    out = agent(bullets=bullets)
    # No greeting name but greeting still present
    assert re.match(r"Good (morning|afternoon|evening),", out["email"])
    # Body contains Changes list
    assert "- One" in out["email"] and "- Two" in out["email"]

