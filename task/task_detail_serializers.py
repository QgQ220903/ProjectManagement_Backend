# task/task_detail_serializers.py
from django.conf import settings  # Thêm dòng này
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
        doers_assignments = obj.task_assignments.filter(role='DOER').select_related('employee').prefetch_related('task_assignment_file__file')
        doers_data = []
        
        request = self.context.get('request')
        
        for assignment in doers_assignments:
            employee_data = EmployeeSerializer(assignment.employee).data
            file_details = assignment.task_assignment_file.all()
            
            files = []
            for fd in file_details:
                if not fd.file or not fd.file.link:
                    continue
                    
                try:
                    # Lấy đường dẫn đầy đủ
                    if request:
                        file_url = fd.file.link.url
                        absolute_url = request.build_absolute_uri(file_url)
                    else:
                        # Fallback nếu không có request (ví dụ trong shell)
                        absolute_url = settings.SITE_URL + fd.file.link.url
                        
                    files.append({
                        'id': fd.file.id,
                        'link': absolute_url,  # Sử dụng absolute_url thay vì đường dẫn tương đối
                        'name': fd.file.name,
                        'status': fd.status,
                        'uploaded_at': fd.file.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    })
                except Exception as e:
                    print(f"Error processing file {fd.file.name if fd.file else 'unknown'}: {str(e)}")
                    continue
            
            doers_data.append({
                **employee_data,
                'status': assignment.status,
                'files': files
            })
        
        return doers_data