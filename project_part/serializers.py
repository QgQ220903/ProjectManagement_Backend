# projects/serializers.py
from rest_framework import serializers
from .models import ProjectPart
from task.serializers import TaskSerializer
class ProjectPartSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = ProjectPart
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_tasks(self, obj):
        tasks = obj.tasks.filter(is_deleted=False, parent_task__isnull=True).order_by('-created_at')
        serializer = TaskSerializer(tasks, many=True)
        return serializer.data