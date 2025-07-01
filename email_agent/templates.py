import random
from typing import List

GREETINGS: List[str] = [
    "Hi", "Hello", "Good morning", "Good afternoon", "Good evening", "Greetings"
]
CLOSINGS: List[str] = [
    "Best regards", "Sincerely", "Thank you", "Kind regards", "Warm regards", "Warmly"
]
# Phrases to introduce the purpose of the email
PURPOSE_INTROS: List[str] = [
    "I wanted to let you know that", "Just a quick update to say that",
    "I’m reaching out to share that", "Please note that"
]
# Phrases to introduce detail points
POINT_INTROS: List[str] = [
    "I have", "Here's an update on", "Please note", "FYI"
]

def pick(items: List[str]) -> str:
    """
    Selects a random item from a non-empty list.
    Raises ValueError if the list is empty.
    """
    if not items:
        raise ValueError("No items to choose from")
    return random.choice(items)
