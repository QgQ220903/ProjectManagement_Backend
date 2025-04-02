from django.db import models
from file.models import File
from task_assignment.models import TaskAssignment
# Create your models here.
class FileDetail(models.Model):
    STATUS_CHOICES = (
        ('IN_PROGRESS', 'Đang thực hiện'),
        ('REVIEW', 'Đang xem xét'),
        ('DONE', 'Hoàn thành'),
    )
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='file_detail', verbose_name="file")
    task_assignment = models.ForeignKey(TaskAssignment, on_delete=models.CASCADE, related_name='task_assignment_file', verbose_name="Công việc được giao")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')

    def __str__(self):
        return f"{self.file} - {self.task_assignment}"

    class Meta:
        db_table = 'file_details'
        verbose_name = "chi tiết file"
        verbose_name_plural = "Các chi tiết file"