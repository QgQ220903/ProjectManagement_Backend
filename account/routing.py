from django.urls import re_path
from .consumers import AccountConsumer

websocket_urlpatterns = [
    re_path(r'ws/account/$', AccountConsumer.as_asgi()),
]
