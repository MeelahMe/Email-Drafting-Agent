import random
from typing import List

GREETINGS: List[str] = ["Hi", "Hello", "Good afternoon", "Greetings"]
CLOSINGS: List[str] = ["Best regards", "Sincerely", "Thank you", "Kind regards"]

def pick(items: List[str]) -> str:
    """
    Selects a random item from a non-empty list.
    Raises ValueError if the list is empty.
    """
    if not items:
        raise ValueError("No items to choose from")
    return random.choice(items)
