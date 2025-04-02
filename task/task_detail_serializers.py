# task/task_detail_serializers.py
from rest_framework import serializers
from .models import Task
from task_assignment.serializers import TaskAssignmentSerializer
from rest_framework import serializers
from task_assignment.serializers import TaskAssignmentSerializer
from employee.serializers import EmployeeSerializer

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
            'responsible_person', 'doers', 'task_assignments', 'project_part',
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