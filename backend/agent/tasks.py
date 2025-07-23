import os
import dramatiq
from pathlib import Path
from django.conf import settings
from chat.models import Message
from chat.utils import push_ws
from .nlu import parse_intent
from .schemas import Intent
from browser.gmail import send_gmail

@dramatiq.actor
def process_user_message(message_id:str):
    msg = Message.objects.get(pk=message_id)
    conv = msg.conversation

    # 1. Parse intent
    intent: Intent = parse_intent(msg.content)
    if intent.needs:
        missing = ', '.join(intent.needs)
        reply = Message.objects.create(conversation=conv, role='agent', content=f"I need: {missing}. Please provide.")
        push_ws(conv.id, 'message.new', {
            'id': str(reply.id), 'role':'agent', 'content': reply.content
        })
        return

    # 2. Execute gmail flow
    creds = { 'email': intent.slots.email, 'password': intent.slots.password }
    email_data = {
        'recipient': intent.slots.recipient,
        'subject': intent.slots.subject,
        'body': intent.slots.body,
    }

    shots_dir = Path(settings.MEDIA_ROOT) / str(conv.id)

    def ws_push(t, payload):
        if 'image_path' in payload:
            # persist message
            m = Message.objects.create(conversation=conv, role='screenshot', image_path=payload['image_path'])
            payload.update({'id':str(m.id), 'role':'screenshot', 'image_url': settings.MEDIA_URL + payload['image_path'].split(str(settings.MEDIA_ROOT))[-1]})
        elif 'content' in payload and payload.get('role') == 'agent':
            m = Message.objects.create(conversation=conv, role='agent', content=payload['content'])
            payload.update({'id':str(m.id)})
        push_ws(conv.id, t, payload)

    ws_push('status.update', {'msg':'Starting browser...'})
    send_gmail(str(conv.id), shots_dir, creds, email_data, ws_push)