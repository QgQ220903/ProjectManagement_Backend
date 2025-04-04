"""
ASGI config for projectmanagement_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import django

# Thiết lập biến môi trường trước khi import bất kỳ module Django nào
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projectmanagement_backend.settings")
django.setup()  # Gọi setup() trước khi import các module Django khác

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import employee.routing
import message.routing
import department.routing
import project.routing
import project_part.routing
import task_assignment.routing
# Gộp tất cả WebSocket routes
websocket_urlpatterns = employee.routing.websocket_urlpatterns + message.routing.websocket_urlpatterns+ department.routing.websocket_urlpatterns + project.routing.websocket_urlpatterns + project_part.routing.websocket_urlpatterns +task_assignment.routing.websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

