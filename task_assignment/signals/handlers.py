from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ..models import TaskAssignment

@receiver(post_save, sender=TaskAssignment)
@receiver(post_delete, sender=TaskAssignment)
def update_task_on_assignment_change(sender, instance, **kwargs):
    """Khi assignment thay đổi -> cập nhật task liên quan"""
    instance.task.update_completion()