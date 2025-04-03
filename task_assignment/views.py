from rest_framework.response import Response  # Thêm dòng này
from rest_framework import viewsets
from .models import TaskAssignment
from .serializers import TaskAssignmentSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
class TaskAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAssignment.objects.all()
    serializer_class = TaskAssignmentSerializer


    def notify_ws_clients(self, action, instance):
        """
        Gửi thông báo WebSocket khi có thay đổi trong TaskAssignment.
        """
        channel_layer = get_channel_layer()
        serializer = self.get_serializer(instance)
        async_to_sync(channel_layer.group_send)(
            "task_assignments",  # Đảm bảo group là 'task_assignments'
            {
                "type": "task_assignment_update",
                "action": action,
                "data": serializer.data,
            }
        )

    def perform_create(self, serializer):
        instance = serializer.save()
        self.notify_ws_clients("create", instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self.notify_ws_clients("update", instance)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        self.notify_ws_clients("delete", instance)



    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_status = instance.status
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        if old_status != instance.status:
            instance.task.update_completion()  # Đảm bảo gọi đúng tên phương thức
        
        return Response(serializer.data)  # Sửa thành Response (đã import)