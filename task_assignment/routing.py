from django.urls import re_path
from .consumers import TaskAssignmentConsumer

websocket_urlpatterns = [
    re_path(r"ws/task_assignments/$", TaskAssignmentConsumer.as_asgi()),  # Định tuyến WebSocket cho TaskAssignment
]
