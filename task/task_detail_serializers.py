# task/task_detail_serializers.py
from rest_framework import serializers
from .models import Task
from task_assignment.serializers import TaskAssignmentSerializer

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = serializers.SerializerMethodField()
    task_assignments = TaskAssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_subtasks(self, obj):
        subtasks = Task.objects.filter(parent_task=obj, is_deleted=False).exclude(id=obj.id)
        serializer = TaskDetailSerializer(subtasks, many=True)
        return serializer.data