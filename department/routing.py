from django.urls import re_path
from .consumers import DepartmentConsumer

websocket_urlpatterns = [
    re_path(r'ws/departments/$', DepartmentConsumer.as_asgi()),
]
