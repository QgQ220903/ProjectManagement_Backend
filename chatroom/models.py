from django.db import models
from task.models import Task
# Create your models here.
class ChatRoom(models.Model):
    task = models.OneToOneField(Task, related_name='chatroom', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"ChatRoom for task {self.task.name}"

    class Meta:
      db_table = 'chatrooms'
      verbose_name = "Phòng chat"
      verbose_name_plural = "Các phòng chat"