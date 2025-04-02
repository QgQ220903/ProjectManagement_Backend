from django.db import models
from chatroom.models import ChatRoom
from employee.models import Employee
from file.models import File
# Create your models here.
class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(Employee, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    file = models.ForeignKey(File, related_name='messages', null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.name} at {self.timestamp}"
    class Meta:
        db_table = 'messages'
        verbose_name = "Tin nhắn"
        verbose_name_plural = "Các tin nhắn"