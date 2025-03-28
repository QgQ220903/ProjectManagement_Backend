# work_history/serializers.py
from rest_framework import serializers
from .models import WorkHistory
from task.serializers import TaskSerializer
from task.models import Task

class WorkHistorySerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)

    class Meta:
        model = WorkHistory
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['task'] = TaskSerializer(instance.task).data if instance.task else None
        return representation

class WorkHistoryCreateSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = WorkHistory
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']