from django.urls import re_path
from .consumers import ProjectPartConsumer

websocket_urlpatterns = [
    re_path(r'ws/project-parts/$', ProjectPartConsumer.as_asgi()),
]
