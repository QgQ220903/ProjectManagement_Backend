from django.urls import re_path
from .consumers import FileDetailConsumer

websocket_urlpatterns = [
    re_path(r'ws/file-detail/$', FileDetailConsumer.as_asgi()),
]
