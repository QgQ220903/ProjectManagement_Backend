# task/task_detail_serializers.py
from rest_framework import serializers
from .models import Task
from task_assignment.serializers import TaskAssignmentSerializer

# class TaskDetailSerializer(serializers.ModelSerializer):
#     subtasks = serializers.SerializerMethodField()
#     task_assignments = TaskAssignmentSerializer(many=True, read_only=True)
    
#     class Meta:
#         model = Task
#         fields = '__all__'
#         read_only_fields = ['created_at', 'updated_at', 'completion_percentage']

#     def get_subtasks(self, obj):
#         subtasks = obj.subtasks.filter(is_deleted=False)
#         serializer = TaskDetailSerializer(subtasks, many=True)
#         return serializer.data

from rest_framework import serializers
from task_assignment.serializers import TaskAssignmentSerializer
from employee.serializers import EmployeeSerializer

# class TaskDetailSerializer(serializers.ModelSerializer):
#     # Hiển thị subtasks dạng lồng nhau
#     subtasks = serializers.SerializerMethodField()
    
#     # Hiển thị người chịu trách nhiệm (RESPONSIBLE)
#     responsible_person = serializers.SerializerMethodField()
    
#     # Hiển thị nhóm thực hiện (DOER)
#     doers = serializers.SerializerMethodField()
    
#     # Hiển thị tất cả phân công (nếu cần)
#     task_assignments = TaskAssignmentSerializer(source='task_assignments', many=True, read_only=True)
#     class Meta:
#         model = Task
#         fields = [
#             'id', 'name', 'description', 'priority', 
#             'start_time', 'end_time', 'task_status',
#             'completion_percentage', 'subtasks',
#             'responsible_person', 'doers', 'assignments',
#             'created_at', 'updated_at'
#         ]
#         read_only_fields = ['created_at', 'updated_at']

#     def get_subtasks(self, obj):
#         """Lấy danh sách subtask dạng lồng nhau"""
#         subtasks = obj.subtasks.filter(is_deleted=False)
#         return TaskDetailSerializer(subtasks, many=True).data

#     def get_responsible_person(self, obj):
#         """Lấy người chịu trách nhiệm (role=RESPONSIBLE)"""
#         assignment = obj.task_assignments.filter(role='RESPONSIBLE').first()
#         return EmployeeSerializer(assignment.employee).data if assignment else None

#     def get_doers(self, obj):
#         """Lấy danh sách người thực hiện (role=DOER)"""
#         doers = obj.task_assignments.filter(role='DOER')
#         return EmployeeSerializer([a.employee for a in doers], many=True).data

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = serializers.SerializerMethodField()
    responsible_person = serializers.SerializerMethodField()
    doers = serializers.SerializerMethodField()
    task_assignments = TaskAssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'priority',
            'start_time', 'end_time', 'task_status',
            'completion_percentage', 'subtasks',
            'responsible_person', 'doers', 'task_assignments',
            'created_at', 'updated_at'
        ]

    def get_subtasks(self, obj):
        subtasks = obj.subtasks.filter(is_deleted=False)
        return TaskDetailSerializer(subtasks, many=True).data

    def get_responsible_person(self, obj):
        assignment = obj.task_assignments.filter(role='RESPONSIBLE').first()
        return EmployeeSerializer(assignment.employee).data if assignment else None

    def get_doers(self, obj):
        doers = obj.task_assignments.filter(role='DOER')
        return EmployeeSerializer([a.employee for a in doers], many=True).data