from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ..models import Task

@receiver(post_save, sender=Task)
@receiver(post_delete, sender=Task)
def update_task_hierarchy(sender, instance, **kwargs):
    """Khi task thay đổi -> cập nhật task cha"""
    if instance.parent_task:
        instance.parent_task.update_completion()