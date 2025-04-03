from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Message
from file.models import File
from rest_framework.decorators import api_view
from chatroom.models import ChatRoom

@api_view(["GET"])
def get_chat_history(request, room_name):
    chatroom = get_object_or_404(ChatRoom, task_id=room_name)
    Chats = Message.objects.filter(chatroom=chatroom).order_by("timestamp")
    return JsonResponse(
        [{
            "sender": msg.sender.email,
            "chat": msg.content,
            "name": msg.sender.name,
            "timestamp": msg.timestamp,
            "file": {
                "name": msg.file.name,
                "url": msg.file.link.url
            } if msg.file else None  # Kiểm tra nếu có file mới lấy
        } for msg in Chats],
        safe=False,
    )