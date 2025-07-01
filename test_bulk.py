import os
import sys

# Make sure your project root is on the import path
sys.path.append(os.getcwd())

from email_agent.agent import EmailDraftingAgent

agent = EmailDraftingAgent()

test_cases = [
    "• Recipient: Alice\n• Purpose: Meeting recap\n• Discussed agenda items\n• Next steps: share notes",
    "• Recipient: Bob\n• Purpose: Project kickoff\n• Scheduled kickoff call\n• CC: Charlie",
    "• Recipient: Clara\n• Purpose: Budget review\n• Reviewed Q1 finances\n• Attached: budget.xlsx",
    "• Recipient: Daniel\n• Purpose: Follow-up\n• Sent proposal\n• Waiting for approval by Friday",
    "• Recipient: Eva\n• Purpose: Event invitation\n• Venue: Main Hall\n• RSVP by Tuesday",
    "• Recipient: Frank\n• Purpose: Thank you\n• Received your feedback\n• Very helpful suggestions",
    "• Recipient: Grace\n• Purpose: Status update\n• Completed module A\n• Starting module B now",
]

for bullets in test_cases:
    out = agent(bullets, sender_name="Jameelah Mercer")
    print("=" * 60)
    print("BULLETS:\n", bullets)
    print("\nSUBJECT:", out["subject"])
    print("\nEMAIL:\n", out["email"])
    print("=" * 60 + "\n")

