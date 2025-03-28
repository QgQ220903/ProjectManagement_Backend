# work_history/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from task.models import Task
from task_assignment.models import TaskAssignment
from .models import WorkHistory

@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    if created:
        responsible_members = TaskAssignment.objects.filter(task=instance, role='RESPONSIBLE')
        doer_members = TaskAssignment.objects.filter(task=instance, role='DOER')

        responsible_names = ", ".join([member.employee.name for member in responsible_members])
        doer_names = ", ".join([member.employee.name for member in doer_members])

        content = f"Khởi tạo công việc '{instance.name}'. "
        if responsible_names:
            content += f"Người đảm nhiệm: {responsible_names}. "
        if doer_names:
            content += f"Thành viên tham gia: {doer_names}."

        WorkHistory.objects.create(task=instance, updated_date=instance.created_at, content=content)

@receiver(post_save, sender=TaskAssignment)
def task_assignment_post_save(sender, instance, created, **kwargs):
    if created:
        content = f"Phân công công việc '{instance.task.name}' cho nhân viên '{instance.employee.name}' với vai trò '{instance.role}'."
        WorkHistory.objects.create(task=instance.task, updated_date=instance.created_at, content=content)