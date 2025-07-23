import os
import json
from openai import OpenAI
from .schemas import Intent, EmailSlots

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

SYSTEM = "You extract intents (send_email/other) and slots from user text. Return JSON only."

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

def parse_intent(message: str) -> Intent:
    prompt = f"User: {message}\nReturn JSON like: {json.dumps(EXAMPLE_SCHEMA)}"
    
    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt}
        ],
        max_output_tokens=400
    )
    
    txt = resp.output_text.strip()
    
    try:
        data = json.loads(txt)
    except Exception:
        data = EXAMPLE_SCHEMA

    needs = []
    slots = EmailSlots(**data.get('slots', {}))

    if data.get('name') == 'send_email':
        for k in ["email", "password", "recipient", "subject", "body"]:
            if getattr(slots, k) in [None, ""]:
                needs.append(k)

    return Intent(name=data.get('name', 'other'), slots=slots, needs=needs)
