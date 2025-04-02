import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import Message, ChatRoom
from employee.models import Employee
from file.models import File
from django.db import models
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Tạo phòng chat nếu chưa tồn tại
        await self.get_or_create_room(self.room_name)

        # Thêm user vào nhóm chat
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Xóa user khỏi nhóm chat
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        chat = data["message"]  # Đổi từ "chat" thành "message"
        sender_id = data["sender"]
        file_id = data.get("file")  # Dùng .get() để tránh KeyError nếu không có "file"
        
        print(f"Received message: {chat}, from: {sender_id}, file: {file_id}") 

        # Kiểm tra sender có tồn tại không
        sender = await sync_to_async(lambda: Employee.objects.get(id=sender_id))()
        if not sender:
            print(f"Sender with ID {sender_id} not found!")
            return  # Dừng lại nếu không tìm thấy sender

        # Nếu file_id có giá trị, lấy file; nếu không, đặt file là None
        file = None
        if file_id:
            try:
                file = await sync_to_async(lambda: File.objects.get(id=file_id))()
            except File.DoesNotExist:
                print(f"File with ID {file_id} not found!")

        print(f"Sender: {sender.email}") 

        # Gửi tin nhắn đến group WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": chat,
                "sender": sender.email,
                "file": file.link if file else None,  # Nếu không có file, trả về None
            },
        )

        # Lưu tin nhắn vào database (nếu có file thì lưu file_id, nếu không thì lưu None)
        await self.save_message(self.room_name, sender.id, chat, file.id if file else None)


    async def chat_message(self, event):
        message = event["message"]
        sender_email = event["sender"]  # Lấy email thay vì object

        # Gửi tin nhắn qua WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender": sender_email}))


    @sync_to_async
    def get_or_create_room(self, room_name):
        """Tạo phòng chat nếu chưa tồn tại"""
        ChatRoom.objects.get_or_create(task_id=room_name)

    @sync_to_async
    def save_message(self, room_name, sender_id, message, file_id):
        """Lưu tin nhắn vào database"""
        room = ChatRoom.objects.get(task_id=room_name)
        sender, _ = Employee.objects.get_or_create(id=sender_id)

        # Nếu file_id có giá trị, lấy file; nếu không thì đặt file = None
        file = None
        if file_id:
            file = File.objects.filter(id=file_id).first()  # Dùng .filter().first() để tránh lỗi nếu không có file

        # Lưu tin nhắn vào database
        Message.objects.create(chatroom=room, sender=sender, content=message, file=file)



