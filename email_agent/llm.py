import os
from openai import OpenAI, OpenAIError

_client = OpenAI()


def polish_email(subject: str, greeting: str, body: str, closing: str) -> str:
    prompt = (
        "Turn the following into a concise, professional email:\n"
        f"Subject: {subject}\n"
        f"{greeting}\n\n"
        f"{body}\n\n"
        f"{closing}\n"
    )
    try:
        resp = _client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip()
    except OpenAIError:
        # Fallback to rule-based
        return f"{greeting}\n\n{body}\n\n{closing}"
