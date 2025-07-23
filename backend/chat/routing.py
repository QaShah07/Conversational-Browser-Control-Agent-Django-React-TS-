from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/conversation/(?P<conv_id>[0-9a-f-]+)/$", consumers.ChatConsumer.as_asgi()),
]