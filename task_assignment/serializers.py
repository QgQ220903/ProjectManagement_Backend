# task_assignment/serializers.py
from rest_framework import serializers
from .models import TaskAssignment
from employee.serializers import EmployeeSerializer  # Import EmployeeSerializer
from task.serializers import TaskSerializer # Import TaskSerializer
from employee.models import Employee
from task.models import Task

class TaskAssignmentSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = TaskAssignment
        fields = ['id', 'employee', 'task', 'role', 'status']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['employee'] = EmployeeSerializer(instance.employee).data
        representation['task'] = TaskSerializer(instance.task).data
        return representation