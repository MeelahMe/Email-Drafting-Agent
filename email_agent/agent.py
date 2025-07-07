# File: email_agent/agent.py
import re
from datetime import datetime
from email_agent.nlg import rewrite_purpose, rewrite_detail
from .subject_transformer import rewrite_subject_segments

COMPOUND_KEYS = {
    "Milestones","Dependencies","Deliverables","Context",
    "Next steps","Steps","Action items","Puntos",
    "Tareas completadas","Links","Risks","Sample payload",
}

MAX_BULLET_LEN = 200

def join_list(items: list[str]) -> str:
    cleaned = [i.strip().rstrip('.') for i in items if i]
    if not cleaned:
        return ''
    if len(cleaned) == 1:
        return cleaned[0]
    if len(cleaned) == 2:
        return f"{cleaned[0]} and {cleaned[1]}"
    return ", ".join(cleaned[:-1]) + f", and {cleaned[-1]}"

def _parse_bullets(bullets: str) -> dict[str, str|list[str]]:
    data, key = {}, None
    for line in bullets.splitlines():
        s = line.strip()
        if s.startswith('•'):
            if ':' in s[1:]: k, v = s[1:].split(':', 1)
            else: k, v = s[1:], ''
            key = k.strip()
            data[key] = v.strip()
        elif key and (s.startswith(('-', '*')) or re.match(r'\d+\.', s)):
            item = re.sub(r'^[\-\*\d\.\s]+', '', s).strip()
            prev = data[key]
            data[key] = prev + [item] if isinstance(prev, list) else ([prev, item] if prev else [item])
        elif key:
            prev = data[key]
            if isinstance(prev, list): prev[-1] += f" {s}"
            else: data[key] = f"{prev} {s}"
    return data

def _make_greeting(recipient: str, lang: str) -> str:
    hr = datetime.now().hour
    if lang.startswith('es'):
        sal = 'Buenos días' if hr < 12 else 'Buenas tardes' if hr < 18 else 'Buenas noches'
    else:
        sal = 'Good morning' if hr < 12 else 'Good afternoon' if hr < 18 else 'Good evening'
    parts = [p.strip().split(',', 1)[0] for p in re.split(r'[;,]', recipient) if p.strip()]
    nm = join_list(parts)
    return f"{sal} {nm}," if nm else f"{sal},"

def _rewrite_purpose_full(purpose: str, tone: str, lang: str) -> str:
    return rewrite_purpose(purpose.strip().rstrip('.'), lang)

def _select_closing(tone: str, lang: str, sender: str) -> str:
    opts_es = {'friendly': 'Saludos', 'urgent': 'Gracias por su pronta atención'}
    opts_en = {'friendly': 'Best regards', 'urgent': 'Thank you for your immediate attention'}
    closing = (opts_es if lang.startswith('es') else opts_en).get(tone.lower(), 'Sincerely')
    return f"{closing},\n{sender}"

class EmailDraftingAgent:
    def __call__(self, bullets: str, sender_name='Your Name', tone='formal', language='en') -> dict:
        # Normalize language
        lang = language.lower()
        if not (lang.startswith('en') or lang.startswith('es')):
            lang = 'en'
        # Empty guard
        if not bullets or not bullets.strip():
            subj = 'No content to send'
            greet = _make_greeting('', lang)
            body = ['It looks like you didn’t provide any details. Please add bullet points and try again.']
            close = _select_closing(tone, lang, sender_name)
            email = f"{greet}\n\n" + "\n\n".join(body) + f"\n\n{close}"
            return {'subject': subj, 'email': email}
        # Parse & truncate
        data = _parse_bullets(bullets)
        for k, v in list(data.items()):
            if isinstance(v, str) and len(v) > MAX_BULLET_LEN:
                data[k] = v[:MAX_BULLET_LEN].rstrip() + '…'
            elif isinstance(v, list):
                data[k] = [i[:MAX_BULLET_LEN].rstrip() + '…' if isinstance(i, str) and len(i) > MAX_BULLET_LEN else i for i in v]
        # Subject
        raw = data.get('Purpose', '').strip().rstrip('.') or 'Update'
        subject = rewrite_subject_segments(raw)
        if tone.lower() == 'urgent':
            subject = f"URGENT: {subject}"
        # Greeting
        rec = data.get('Recipient') or data.get('Recipients', '')
        greet = _make_greeting(rec, lang)
        # Build body
        lines: list[str] = []
        # Purpose
        pur = data.get('Purpose', '').strip()
        if pur:
            lines.append(_rewrite_purpose_full(pur, tone, lang))
        # Additional bullets
        skipped = {'Recipient', 'Recipients', 'Purpose', 'Attachment', 'Attached'}
        extras = [k for k in data.keys() if k not in skipped]
        if pur and not extras:
            lines.append(f"• {pur}")
        for k in extras:
            v = data[k]
            if isinstance(v, str) and not v.strip():
                lines.append(f"• {k}")
            elif isinstance(v, str) and v.endswith('…'):
                lines.append(f"• {v}")
            elif isinstance(v, list):
                for i in v:
                    lines.append(f"• {rewrite_detail(i, lang)}")
            elif isinstance(v, str):
                lines.append(f"• {rewrite_detail(v, lang)}")
        # Attachment
        att = data.get('Attachment') or data.get('Attached')
        if att:
            lines.append(f"Please find the attached {att}.")
        # Closing
        close = _select_closing(tone, lang, sender_name)
        # Assemble
        email = f"{greet}\n\n" + "\n\n".join(lines) + f"\n\n{close}"
        return {'subject': subject, 'email': email}


