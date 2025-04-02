from rest_framework import serializers
from .models import Task
from employee.serializers import EmployeeSerializer

class EmployeeLeafTaskSerializer(serializers.ModelSerializer):
    responsible_person = serializers.SerializerMethodField()
    doers = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'priority',
            'start_time', 'end_time', 'task_status',
            'completion_percentage', 'subtasks',
            'responsible_person', 'doers',
            'project_part', 'created_at', 'updated_at'
        ]

    def get_responsible_person(self, obj):
        assignment = obj.task_assignments.filter(role='RESPONSIBLE').first()
        return EmployeeSerializer(assignment.employee).data if assignment else None

    def get_doers(self, obj):
        doers = obj.task_assignments.filter(role='DOER')
        return EmployeeSerializer([a.employee for a in doers], many=True).data