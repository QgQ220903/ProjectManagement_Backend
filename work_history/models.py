# work_history/models.py
from django.db import models
from task.models import Task

class WorkHistory(models.Model):
    history_code = models.AutoField(primary_key=True, verbose_name="Mã lịch sử công việc")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='work_histories', verbose_name="Mã công việc")
    updated_date = models.DateTimeField(verbose_name="Ngày cập nhật")
    content = models.TextField(verbose_name="Nội dung")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    def __str__(self):
        return f"{self.history_code} - {self.task} - {self.updated_date}"

    class Meta:
        db_table = 'work_histories'
        verbose_name = "Lịch sử công việc"
        verbose_name_plural = "Các lịch sử công việc"