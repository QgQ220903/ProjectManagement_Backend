from rest_framework import viewsets, filters, response
from task_assignment.serializers import TaskAssignmentSerializer
from task_assignment.models import TaskAssignment
from .models import Task
from .serializers import TaskSerializer  # Thêm dòng này
from .task_detail_serializers import TaskDetailSerializer
from rest_framework.decorators import action
from rest_framework import status
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

    @action(detail=False, methods=['GET'], url_path='employee-leaf-tasks/(?P<employee_id>[^/.]+)')
    def get_employee_leaf_tasks(self, request, employee_id=None):
        """
        Lấy tất cả công việc con thấp nhất (không có subtask) của một nhân viên
        """
        try:
            # Lấy tất cả task assignment của nhân viên
            assignments = TaskAssignment.objects.filter(
                employee_id=employee_id,
                is_deleted=False
            ).select_related('task')
            
            leaf_tasks = []
            
            for assignment in assignments:
                task = assignment.task
                # Kiểm tra nếu task không có subtask (là leaf task)
                if not task.subtasks.exists():
                    leaf_tasks.append(task)
            
            # Serialize dữ liệu
            serializer = TaskDetailSerializer(leaf_tasks, many=True, context={'request': request})
            
            return response.Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return response.Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return TaskDetailSerializer
        return TaskSerializer