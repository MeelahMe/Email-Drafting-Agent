from typing import Dict, List


def parse_bullets(raw: str) -> Dict[str, object]:
    """
    Parses bullet-point text into a structured dictionary.

    Args:
        raw: Multiline string with bullet points. Each line may start with '•', '-', or whitespace.

    Returns:
        A dict with keys:
            - 'recipient': extracted recipient name (empty string if not found)
            - 'purpose': extracted purpose/subject (empty string if not found)
            - 'points': list of detail strings (without trailing punctuation)
    """
    result: Dict[str, object] = {"recipient": "", "purpose": "", "points": []}
    for line in raw.splitlines():
        text = line.lstrip("•- \t").strip()
        if not text:
            continue
        lowered = text.lower()
        if lowered.startswith(("recipient:", "to:")):
            _, value = text.split(":", 1)
            result["recipient"] = value.strip()
        elif lowered.startswith(("purpose:", "subject:")):
            _, value = text.split(":", 1)
            result["purpose"] = value.strip()
        else:
            # Remove trailing period if present
            point = text.rstrip(".")
            result["points"].append(point)
    return result
