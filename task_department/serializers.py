# task_department/serializers.py
from rest_framework import serializers
from .models import DepartmentTask
from department.serializers import DepartmentSerializer
from task.serializers import TaskSerializer
from task.models import Task
from department.models import Department

class DepartmentTaskSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = DepartmentTask
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['department'] = DepartmentSerializer(instance.department).data if instance.department else None
        representation['task'] = TaskSerializer(instance.task).data if instance.task else None
        return representation

class DepartmentTaskCreateUpdateSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = DepartmentTask
        fields = '__all__'