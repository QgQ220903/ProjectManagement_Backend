# task_assignment/serializers.py
from rest_framework import serializers
from .models import TaskAssignment
from employee.serializers import EmployeeSerializer  # Import EmployeeSerializer
from task.serializers import TaskSerializer # Import TaskSerializer

class TaskAssignmentSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)  # Sử dụng EmployeeSerializer
    task = TaskSerializer(read_only=True)

    class Meta:
        model = TaskAssignment
        fields = ['id', 'employee', 'task', 'role', 'status']