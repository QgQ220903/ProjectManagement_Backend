from rest_framework import viewsets, filters, response

from task_assignment.serializers import TaskAssignmentSerializer
from task_assignment.models import TaskAssignment
from .models import Task

from .serializers import TaskSerializer,TaskStatisticsFilterSerializer  # Thêm dòng này
from .task_detail_serializers import TaskDetailSerializer
from .employee_leaf_task_serializers import EmployeeLeafTaskSerializer
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.pagination import PageNumberPagination  # Thêm import
from department.models import Department
from project_part.models import ProjectPart
from task.models import Task
from django.utils.timezone import now
from rest_framework.response import Response
from django.db.models import Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_task_update(data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "task_updates",
        {
            "type": "send_task_update",
            "message": data
        }
    )


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
        send_task_update({
        "action": "update",
        "task_id": instance.task.id,
        "assignment_id": instance.id,
        "status": instance.status,
        })
        return response.Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):  # Thêm class mới này để xử lý Task
    queryset = Task.objects.filter(is_deleted=False).order_by('-created_at')



    @action(detail=False, methods=['GET'], url_path='employee-leaf-tasks/(?P<employee_id>[^/.]+)')
    def get_employee_leaf_tasks(self, request, employee_id=None):
        try:
            assignments = TaskAssignment.objects.filter(
                employee_id=employee_id,
                is_deleted=False,
                role='DOER'
            ).select_related('task')

            leaf_tasks = []

            for assignment in assignments:
                task = assignment.task
                if not task.subtasks.exists():
                    # Gán thêm assignment_id vào task
                    task.assignment_id = assignment.id  # Lưu assignment_id vào object
                    leaf_tasks.append(task)

            serializer = EmployeeLeafTaskSerializer(
                leaf_tasks, many=True, context={'request': request, 'employee_id': employee_id}
            )

            return response.Response({
                'success': True,
                'count': len(leaf_tasks),
                'data': serializer.data
            })

        except Exception as e:
            return response.Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return TaskDetailSerializer
        return TaskSerializer
    

    def perform_create(self, serializer):
        task = serializer.save()
        send_task_update({
            "action": "create",
            "task": TaskSerializer(task).data
        })

    def perform_update(self, serializer):
        task = serializer.save()
        send_task_update({
            "action": "update",
            "task": TaskSerializer(task).data
        })

    def perform_destroy(self, instance):
        task_id = instance.id
        instance.delete()
        send_task_update({
            "action": "delete",
            "task_id": task_id
        })
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    




class TaskStatisticsViewSet(viewsets.ViewSet):
    serializer_class = TaskStatisticsFilterSerializer

    @action(detail=False, methods=['post'], url_path='by-all-department')
    def by_department(self, request):
        serializer = TaskStatisticsFilterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data
        start_date = validated['start_date']
        end_date = validated['end_date']
        now_time = now()

        results = []
        departments = Department.objects.filter(is_deleted=False)
        for dept in departments:
            tasks = Task.objects.filter(
                Q(start_time__range=(start_date, end_date)) |
                Q(end_time__range=(start_date, end_date)),
                project_part__department=dept,
                is_deleted=False
            )

            done = tasks.filter(completion_percentage=100).count()
            delayed = tasks.filter(
                completion_percentage__lt=100,
                end_time__lt=now_time
            ).count()

            results.append({
                "department_id": dept.id,
                "department_name": dept.name,
                "total_tasks": tasks.count(),
                "done": done,
                "delayed": delayed,
                "in_process": tasks.count()-done-delayed,
            })

        return Response(results)

    @action(detail=False, methods=['post'], url_path='by-all-project-part')
    def by_project_part(self, request):
        serializer = TaskStatisticsFilterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data
        start_date = validated['start_date']
        end_date = validated['end_date']
        now_time = now()

        results = []
        project_parts = ProjectPart.objects.filter(is_deleted=False)
        for part in project_parts:
            tasks = Task.objects.filter(
                Q(start_time__range=(start_date, end_date)) |
                Q(end_time__range=(start_date, end_date)),
                project_part=part,
                is_deleted=False
            )

            done = tasks.filter( completion_percentage=100).count()
            delayed = tasks.filter(
                completion_percentage__lt=100,
                end_time__lt=now_time
            ).count()

            results.append({
                "project_part_id": part.id,
                "project_part_name": part.name,
                "department_id": part.department.id if part.department else None,
                "department_name": part.department.name if part.department else None,
                "total_tasks": tasks.count(),
                "done": done,
                "delayed": delayed,
                "in_process": tasks.count() - done - delayed,
            })

        return Response(results)

from django.db import connection
class TaskReportViewSet(viewsets.ViewSet):
    serializer_class = TaskStatisticsFilterSerializer

    @action(detail=False, methods=['post'], url_path='report')
    def report(self, request):
        serializer = TaskStatisticsFilterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data
        start_date = validated['start_date']
        end_date = validated['end_date']

        with connection.cursor() as cursor:
            query = """
                WITH RECURSIVE task_tree AS (
   
                SELECT 
                    t.id,
                    t.name,
                    t.parent_task_id,
                    0 AS level,
                    CAST(t.name AS CHAR(1000)) AS path,
                    t.completion_percentage,
                    t.created_at,
                    pp.name AS project_part_name
                FROM tasks t
                LEFT JOIN project_parts pp ON t.project_part_id = pp.id
                WHERE t.parent_task_id IS NULL
                AND t.created_at BETWEEN %s AND %s

                UNION ALL

            
                SELECT 
                    t.id,
                    t.name,
                    t.parent_task_id,
                    tt.level + 1,
                    CONCAT(tt.path, ' -> ', t.name),
                    t.completion_percentage,
                    t.created_at,
                    pp.name AS project_part_name
                FROM tasks t
                LEFT JOIN project_parts pp ON t.project_part_id = pp.id
                JOIN task_tree tt ON t.parent_task_id = tt.id
            )

            SELECT 
                tt.id,
                CONCAT(REPEAT('', tt.level), tt.name) AS task_display_name,
                tt.level,
                tt.path, 
                tt.created_at,
                tt.completion_percentage,
                tt.project_part_name,
                GROUP_CONCAT(DISTINCT e.name SEPARATOR ', ') AS employee_names
            FROM task_tree tt
            LEFT JOIN task_assignments ta ON tt.id = ta.task_id
            LEFT JOIN employees e ON ta.employee_id = e.id
            GROUP BY tt.id, tt.name, tt.level, tt.path, tt.created_at, tt.completion_percentage, tt.project_part_name
            ORDER BY tt.path;
            """
            cursor.execute(query, [start_date, end_date])
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response(results)
