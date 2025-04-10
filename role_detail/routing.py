from django.urls import re_path
from .consumers import RoleDetailConsumer

websocket_urlpatterns = [
    re_path(r'ws/role-detail/$', RoleDetailConsumer.as_asgi()),
]
