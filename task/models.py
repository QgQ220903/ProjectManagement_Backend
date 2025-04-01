from django.db import models
from project_part.models import ProjectPart
from django.apps import apps  # Import để tránh vòng lặp

class Task(models.Model):
    PRIORITY_CHOICES = [
        (0, 'Thấp'),
        (1, 'Trung bình'),
        (2, 'Cao'),
    ]

    TASK_STATUS_CHOICES = [
        ('TO_DO', 'Chờ thực hiện'),
        ('IN_PROGRESS', 'Đang thực hiện'),
        ('DONE', 'Hoàn thành'),
        ('CANCELLED', 'Đã hủy'),
        ('ON_HOLD', 'Tạm dừng'),
        ('DELAYED', 'Trễ hạn'),
        ('POSTPONED', 'Trì hoãn'),
    ]

    project_part = models.ForeignKey(ProjectPart, on_delete=models.CASCADE, related_name="tasks")
    parent_task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="subtasks")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    task_status = models.CharField(max_length=50, choices=TASK_STATUS_CHOICES, default='TO_DO')
    completion_percentage = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    def __str__(self):
        return self.name

    def update_completion(self):
        """
        Tính % hoàn thành theo quy tắc:
        - Task có subtask: tính trung bình % hoàn thành của subtask
        - Task không có subtask: tính theo % hoàn thành của assignments hoặc trạng thái
        """
        old_percentage = self.completion_percentage
        
        if self.subtasks.exists():
            # Tính trung bình % hoàn thành của các subtask
            total = self.subtasks.count()
            if total > 0:
                sum_percentage = sum(subtask.completion_percentage for subtask in self.subtasks.all())
                new_percentage = sum_percentage / total
            else:
                new_percentage = 0
        else:
            # Nếu không có subtask, kiểm tra trạng thái
            if self.task_status == 'DONE':
                new_percentage = 100
            elif self.task_status == 'TO_DO':
                new_percentage = 0
            else:
                # Hoặc tính theo assignments nếu có
                completed = self.task_assignments.filter(status='DONE').count()
                total = self.task_assignments.count()
                new_percentage = (completed / total) * 100 if total > 0 else self.completion_percentage
        
        # Làm tròn và đảm bảo trong khoảng 0-100
        new_percentage = max(0, min(100, round(new_percentage)))
        
        # Chỉ cập nhật nếu % thay đổi
        if self.completion_percentage != new_percentage:
            self.completion_percentage = new_percentage
            self.save(update_fields=['completion_percentage'])
        
        # Cập nhật task cha (nếu có)
        if self.parent_task:
            self.parent_task.update_completion()

    class Meta:
        db_table = 'tasks'
        verbose_name = "Công Việc"
        verbose_name_plural = "Các Công Việc"
