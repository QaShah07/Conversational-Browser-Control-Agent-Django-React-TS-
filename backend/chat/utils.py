from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def push_ws(conv_id, type_, payload):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        f'conv_{conv_id}',
        {'type': 'chat_message', 'data': {'type': type_, 'payload': payload}}
    )