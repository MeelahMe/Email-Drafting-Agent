import pytest
from email_agent.nlg import rewrite_purpose, rewrite_detail

@pytest.mark.parametrize("inp,expected", [
    ("Follow-up", "I wanted to follow up on your request."),
    ("Project update", "I'm writing to provide an update on the project."),
    ("Request: timeline", "I'm reaching out with a request regarding timeline."),
    ("New feature launch", "I wanted to let you know about New feature launch."),
])
def test_rewrite_purpose(inp, expected):
    assert rewrite_purpose(inp) == expected

@pytest.mark.parametrize("inp,expected", [
    ("Completed assignment", "I have completed the assignment."),
    ("Attached report.pdf", "Please find the attached report.pdf."),
    ("Finished review", "I have finished the review."),
    ("Call me", "Call me."),
])
def test_rewrite_detail(inp, expected):
    assert rewrite_detail(inp) == expected

