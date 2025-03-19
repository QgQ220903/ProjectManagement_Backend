from django.db import models

class TaskAssignment(models.Model):
    ROLE_CHOICES = (
        ('RESPONSIBLE', 'Người chịu trách nhiệm'),
        ('DOER', 'Người làm'),
    )

    STATUS_CHOICES = (
        ('IN_PROGRESS', 'Đang thực hiện'),
        ('REVIEW', 'Đang xem xét'),
        ('DONE', 'Hoàn thành'),
    )

    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, related_name='task_assignments')
    task = models.ForeignKey('task.Task', on_delete=models.CASCADE, related_name='task_assignments')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Phân công {self.task} cho {self.employee} ({self.role})"
    
    class Meta:
      db_table = 'task_assignments'
      verbose_name = "Phân Công"
