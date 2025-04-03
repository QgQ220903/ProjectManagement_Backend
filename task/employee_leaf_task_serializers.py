from rest_framework import serializers
from .models import Task
from employee.serializers import EmployeeSerializer
from file_detail.models import FileDetail  # Import model FileDetail

class EmployeeLeafTaskSerializer(serializers.ModelSerializer):
    responsible_person = serializers.SerializerMethodField()
    doers = serializers.SerializerMethodField()
    assignment_id = serializers.SerializerMethodField()  # Dùng SerializerMethodField()
    files = serializers.SerializerMethodField()  # Thêm trường files
    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'priority',
            'start_time', 'end_time', 'task_status',
            'completion_percentage', 'subtasks',
            'responsible_person', 'doers', 'files',
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

    def get_files(self, obj):
        request = self.context.get('request')
        employee_id = self.context.get('employee_id')
        
        # Lấy tất cả file của employee này trong task
        file_details = FileDetail.objects.filter(
            task_assignment__task=obj,
            task_assignment__employee_id=employee_id
        ).select_related('file')
        
        files_data = []
        for fd in file_details:
            try:
                file_url = fd.file.link.url
                absolute_url = request.build_absolute_uri(file_url) if request else file_url
                
                files_data.append({
                    'id': fd.file.id,
                    'name': fd.file.name,
                    'link': absolute_url,
                    'status': fd.status,
                    'uploaded_at': fd.file.created_at.strftime("%Y-%m-%d %H:%M:%S")
                })
            except Exception as e:
                continue
        
        return files_data