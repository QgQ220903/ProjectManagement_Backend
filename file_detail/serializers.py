from rest_framework import serializers
from .models import FileDetail
from task_assignment.serializers import TaskAssignmentSerializer
from file.serializers import FileSerializer
from file.models import File
from task_assignment.models import TaskAssignment

class FileDetailSerializer(serializers.ModelSerializer):
    file = FileSerializer(read_only=True)  # Lấy thông tin chi tiết file khi GET
    task_assignment = TaskAssignmentSerializer(read_only=True)  # Lấy thông tin công việc khi GET
    file_id = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), source='file', write_only=True)  
    task_assignment_id = serializers.PrimaryKeyRelatedField(queryset=TaskAssignment.objects.all(), source='task_assignment', write_only=True)  

    class Meta:
        model = FileDetail
        fields = ['id', 'file', 'task_assignment', 'status', 'file_id', 'task_assignment_id']