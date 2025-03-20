# task_department/models.py
from django.db import models
from department.models import Department
from task.models import Task

class DepartmentTask(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_tasks', verbose_name="Phòng ban")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='department_tasks', verbose_name="Công việc")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    def __str__(self):
        return f"{self.department} - {self.task}"

    class Meta:
        db_table = 'department_tasks'
        verbose_name = "Công việc phòng ban"
        verbose_name_plural = "Các công việc phòng ban"