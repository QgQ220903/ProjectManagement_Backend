from rest_framework import serializers
from .models import ProjectPart
from department.serializers import DepartmentSerializer
from task.task_detail_serializers import TaskDetailSerializer
from department.models import Department

class ProjectPartSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()
    archived_tasks = serializers.SerializerMethodField()  # Thêm trường mới
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), 
        write_only=True,
        source='department'  # Thêm source để tự động map khi create/update
    )
    manager_id = serializers.SerializerMethodField()

    class Meta:
        model = ProjectPart
        fields = [
            'id', 'name', 'project', 
            'department', 'department_id', 'manager_id', 
            'is_deleted', 'created_at', 'updated_at',
            'tasks', 'archived_tasks'  # Đảm bảo bao gồm tất cả các trường cần thiết
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_tasks(self, obj):
        tasks = obj.tasks.filter(
            is_deleted=False, 
            parent_task__isnull=True
        ).order_by('-created_at').prefetch_related(
            'task_assignments__employee',
            'subtasks'
        )
        return TaskDetailSerializer(tasks, many=True).data
    
    def get_archived_tasks(self, obj):
        archived_tasks = obj.tasks.filter(
            is_deleted=True,  # Lọc task đã xóa
            parent_task__isnull=True
        ).order_by('-created_at').prefetch_related(
            'task_assignments__employee',
            'subtasks'
        )
        return TaskDetailSerializer(archived_tasks, many=True).data

    def get_manager_id(self, obj):
        return obj.department.manager.id if obj.department and obj.department.manager else None

    # Có thể bỏ phương thức create() vì đã dùng source='department'