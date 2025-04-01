from rest_framework.response import Response  # Thêm dòng này
from rest_framework import viewsets
from .models import TaskAssignment
from .serializers import TaskAssignmentSerializer

class TaskAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAssignment.objects.all()
    serializer_class = TaskAssignmentSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_status = instance.status
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        if old_status != instance.status:
            instance.task.update_completion()  # Đảm bảo gọi đúng tên phương thức
        
        return Response(serializer.data)  # Sửa thành Response (đã import)