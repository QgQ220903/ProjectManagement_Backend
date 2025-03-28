# project_part/serializers.py
from rest_framework import serializers
from .models import ProjectPart
from task.task_detail_serializers import TaskDetailSerializer
from department.models import Department

class ProjectPartSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), required=False)  # Chỉnh sửa để trường department không bắt buộc

    class Meta:
        model = ProjectPart
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_tasks(self, obj):
        tasks = obj.tasks.filter(is_deleted=False, parent_task__isnull=True).order_by('-created_at')
        serializer = TaskDetailSerializer(tasks, many=True)
        return serializer.data
