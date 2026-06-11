from django.urls import re_path
from game.consumers import MyConsumer

websocket_urlpatterns = [
    re_path(r'wss/some_path/', MyConsumer.as_asgi()),
]