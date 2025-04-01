# task_assignment/serializers.py
from rest_framework import serializers
from .models import TaskAssignment
from employee.serializers import EmployeeSerializer  # Import EmployeeSerializer
from task.serializers import TaskSerializer # Import TaskSerializer
from employee.models import Employee
from task.models import Task

# class TaskAssignmentSerializer(serializers.ModelSerializer):
#     employee = EmployeeSerializer(read_only=True)
#     task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())  # Không dùng TaskSerializer để tránh vòng lặp


#     class Meta:
#         model = TaskAssignment
#         fields = ['id', 'employee', 'task', 'role', 'status']
    
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['employee'] = EmployeeSerializer(instance.employee).data
#         representation['task'] = TaskSerializer(instance.task).data
#         return representation

class TaskAssignmentSerializer(serializers.ModelSerializer):
    # Cho phép chọn employee khi viết (POST/PUT)
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        write_only=False  # Mặc định là False, có thể bỏ
    )
    
    # Cho GET hiển thị đầy đủ thông tin
    employee_details = EmployeeSerializer(
        source='employee', 
        read_only=True
    )
    
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    task_details = TaskSerializer(source='task', read_only=True)

    class Meta:
        model = TaskAssignment
        fields = [
            'id', 
            'employee', 'employee_details',
            'task', 'task_details',
            'role', 'status'
        ]