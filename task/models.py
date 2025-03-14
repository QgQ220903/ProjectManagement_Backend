from django.db import models
from project_part.models import ProjectPart

class Task(models.Model):
    project_part = models.ForeignKey(ProjectPart, on_delete=models.CASCADE, related_name='tasks') 
    parent_task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subtasks')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(default=0)  # Ví dụ: 0 (thấp), 1 (trung bình), 2 (cao)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    task_status = models.CharField(max_length=50, default='To Do')  # Ví dụ: To Do, In Progress, Done
    completion_percentage = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tasks'
        verbose_name = "Công Việc"
        verbose_name_plural = "Các Công Việc"