from rest_framework import serializers
from .models import Task
from employee.serializers import EmployeeSerializer

class EmployeeLeafTaskSerializer(serializers.ModelSerializer):
    responsible_person = serializers.SerializerMethodField()
    doers = serializers.SerializerMethodField()
    assignment_id = serializers.SerializerMethodField()  # Dùng SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'priority',
            'start_time', 'end_time', 'task_status',
            'completion_percentage', 'subtasks',
            'responsible_person', 'doers',
            'project_part', 'created_at', 'updated_at',
            'assignment_id'  # Bây giờ nó hợp lệ vì đã khai báo ở trên
        ]

    def get_assignment_id(self, obj):
        """
        Lấy assignment_id của employee đang request
        """
        employee_id = self.context.get('employee_id')
        assignment = obj.task_assignments.filter(employee_id=employee_id, role='DOER').first()
        return assignment.id if assignment else None

    def get_responsible_person(self, obj):
        assignment = obj.task_assignments.filter(role='RESPONSIBLE').first()
        return EmployeeSerializer(assignment.employee).data if assignment else None

    def get_doers(self, obj):
        doers = obj.task_assignments.filter(role='DOER')
        return EmployeeSerializer([a.employee for a in doers], many=True).data
