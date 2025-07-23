import os
import json
import google.generativeai as genai
from .schemas import Intent, EmailSlots

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

EXAMPLE_SCHEMA = {
    "name": "send_email",
    "slots": {
        "recipient": None,
        "subject": None,
        "body": None,
        "start_date": None,
        "end_date": None,
        "reason": None,
        "email": None,
        "password": None
    },
    "needs": []
}

SYSTEM = (
    "You are a JSON-only extractor. Given a user message, output a JSON matching this schema:\n"
    + json.dumps(EXAMPLE_SCHEMA)
)

def _safe_json(text: str):
    try:
        return json.loads(text)
    except Exception:
        # Try to extract the JSON part from raw text
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end+1])
            except Exception:
                pass
        return EXAMPLE_SCHEMA

def parse_intent(message: str) -> Intent:
    prompt = (
        f"SYSTEM:\n{SYSTEM}\n"
        f"USER:\n{message}\n"
        f"Return ONLY the JSON."
    )
    resp = model.generate_content(prompt)
    txt = resp.text.strip()
    data = _safe_json(txt)

    slots = EmailSlots(**data.get('slots', {}))
    needs = []

    if data.get('name') == 'send_email':
        for k in ["email", "password", "recipient", "subject", "body"]:
            if not getattr(slots, k):
                needs.append(k)

    return Intent(name=data.get('name', 'other'), slots=slots, needs=needs)
