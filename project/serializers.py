from rest_framework import serializers
from project.models import Project
from project_part.models import ProjectPart  
from task.models import Task  # Import model Task nếu nó nằm ở app khác

# Serializer cho Task
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'priority', 
            'start_time', 'end_time', 'task_status', 
            'completion_percentage', 'created_at', 'updated_at'
        ]

# Serializer cho ProjectPart, bao gồm danh sách Task
class ProjectPartSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)  # Thêm danh sách Task

    class Meta:
        model = ProjectPart
        fields = ['id', 'name', 'is_deleted', 'created_at', 'updated_at', 'tasks']

# Serializer cho Project, bao gồm danh sách ProjectPart
class ProjectSerializer(serializers.ModelSerializer):
    parts = ProjectPartSerializer(source='projectpart_set', many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'created_at', 'updated_at', 'parts']
