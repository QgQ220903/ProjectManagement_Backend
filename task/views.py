from rest_framework import viewsets, filters, response
from task_assignment.serializers import TaskAssignmentSerializer
from task_assignment.models import TaskAssignment
from .models import Task
from .serializers import TaskSerializer  # Thêm dòng này
from .task_detail_serializers import TaskDetailSerializer

class TaskAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TaskAssignment.objects.all()  # Sửa từ Task.objects... sang TaskAssignment.objects...
    serializer_class = TaskAssignmentSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Nếu trạng thái mới là 'DONE', cập nhật phần trăm task cha
        if instance.status == 'DONE':
            instance.task.update_completion_percentage()

        return response.Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):  # Thêm class mới này để xử lý Task
    queryset = Task.objects.filter(is_deleted=False).order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return TaskDetailSerializer
        return TaskSerializer