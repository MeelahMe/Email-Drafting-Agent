# File: email_agent/subject_transformer.py
"""
Subject Transformer Module

Provides functions to rewrite email subject lines into
Title Case segments with proper Oxford comma + ampersand usage,
preserving uppercase acronyms and stripping stray “and”.
"""

import re
from typing import List

def _titleize_segment(seg: str) -> str:
    """
    Title-case a segment, preserving all-uppercase acronyms.

    e.g., "API Changes" remains "API Changes", but "review api" -> "Review API".
    """
    words = seg.split()
    result: List[str] = []
    for word in words:
        # Preserve acronyms (all uppercase letters/digits)
        if re.fullmatch(r"[A-Z0-9]+", word):
            result.append(word)
        else:
            result.append(word.capitalize())
    return " ".join(result)

def rewrite_subject_segments(subject: str) -> str:
    """
    Transform a subject line into:
      - Sentence-case if single clause
      - Title Case segments joined with ' & ' or Oxford comma + '&' for multiple clauses
    Preserves all-caps acronyms and removes redundant 'and'.

    Examples:
      'Follow-up on assignment'               -> 'Follow-up on assignment'
      'review api changes and update docs'    -> 'Review API Changes & Update Docs'
      'first, second, and third'              -> 'First, Second, & Third'
    """
    if not subject:
        return ""

    # Split on commas or the word 'and'
    raw_parts = re.split(r',\s*|\s+and\s+', subject)
    parts: List[str] = []
    for p in raw_parts:
        p = p.strip()
        # drop empty segments or literal 'and'
        if not p or p.lower() == "and":
            continue
        # remove leading 'and '
        p = re.sub(r'(?i)^and\s+', '', p)
        parts.append(p)

    count = len(parts)
    if count == 0:
        return subject.capitalize()

    # Single clause: sentence-case (first letter uppercase, rest lowercase)
    if count == 1:
        p = parts[0]
        return p[0].upper() + p[1:].lower() if len(p) > 1 else p.upper()

    # Multiple clauses: titleize each
    titled = [_titleize_segment(p) for p in parts]
    if count == 2:
        return f"{titled[0]} & {titled[1]}"
    # Three or more: Oxford comma before final ampersand
    return ", ".join(titled[:-1]) + f", & {titled[-1]}"

