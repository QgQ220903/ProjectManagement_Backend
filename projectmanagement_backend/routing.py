from django.urls import re_path
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
import employee.routing
import message.routing
import department.routing

# websocket_urlpatterns = employee.routing.websocket_urlpatterns + message.routing.websocket_urlpatterns+ department.routing.websocket_urlpatterns

# application = URLRouter(websocket_urlpatterns)  # Chỉ định nghĩa WebSocket routes
