def parse_bullets(raw: str) -> dict:
    """
    Very small heuristic parser.
    Returns {recipient, purpose, points[]} – all strings.
    """
    out = {"recipient": "", "purpose": "", "points": []}
    for line in filter(None, (l.strip("•- \t") for l in raw.splitlines())):
        lower = line.lower()
        if lower.startswith(("recipient:", "to:")):
            out["recipient"] = line.split(":", 1)[1].strip()
        elif lower.startswith(("purpose:", "subject:")):
            out["purpose"] = line.split(":", 1)[1].strip()
        else:
            out["points"].append(line.rstrip("."))
    return out

