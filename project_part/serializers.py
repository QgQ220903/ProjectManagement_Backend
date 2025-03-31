# project_part/serializers.py
from rest_framework import serializers
from .models import ProjectPart
from department.serializers import DepartmentSerializer
from task.task_detail_serializers import TaskDetailSerializer
from department.models import Department

class ProjectPartSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()
    department = DepartmentSerializer(read_only=True)  # Hiển thị chi tiết department khi GET
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), write_only=True)
    class Meta:
        model = ProjectPart
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_tasks(self, obj):
        tasks = obj.tasks.filter(is_deleted=False, parent_task__isnull=True).order_by('-created_at')
        serializer = TaskDetailSerializer(tasks, many=True)
        return serializer.data
    def create(self, validated_data):
        department = validated_data.pop('department_id', None)  # Lấy ID của department từ dữ liệu gửi lên
        project_part = ProjectPart.objects.create(**validated_data, department=department)  # Tạo bản ghi với department đúng kiểu
        return project_part
