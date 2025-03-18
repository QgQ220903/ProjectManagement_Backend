# tasks/serializers.py
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    subtasks = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_subtasks(self, obj):
        subtasks = Task.objects.filter(parent_task=obj, is_deleted=False).exclude(id=obj.id) #Thêm .exclude(id=obj.id)
        serializer = TaskSerializer(subtasks, many=True)
        return serializer.data