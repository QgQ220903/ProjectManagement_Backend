from rest_framework.response import Response  # Thêm dòng này
from rest_framework import viewsets
from .models import TaskAssignment
from .serializers import TaskAssignmentSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_task_assignment_update(action, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "task_assignments",
        {
            "type": "task_assignment_update",
            "action": action,
            "data": data
        }
    )
class TaskAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAssignment.objects.all()
    serializer_class = TaskAssignmentSerializer


    def perform_create(self, serializer):
        instance = serializer.save()
        send_task_assignment_update("create", self.get_serializer(instance).data)

    def perform_update(self, serializer):
        instance = serializer.save()
        send_task_assignment_update("update", self.get_serializer(instance).data)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        send_task_assignment_update("delete", self.get_serializer(instance).data)



    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_status = instance.status
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        if old_status != instance.status:
            instance.task.update_completion()  # Đảm bảo gọi đúng tên phương thức
        send_task_assignment_update("update", self.get_serializer(instance).data)
        return Response(serializer.data)  # Sửa thành Response (đã import)