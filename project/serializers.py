from rest_framework import serializers
from project.models import Project
from project_part.models import ProjectPart  
from project_part.serializers import ProjectPartSerializer
from task.models import Task  # Import model Task nếu nó nằm ở app khác

# Serializer cho Project, bao gồm danh sách ProjectPart
class ProjectSerializer(serializers.ModelSerializer):
    project_parts = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_project_parts(self, obj):
        project_parts = obj.project_parts.filter(is_deleted=False).order_by('-created_at') # Sử dụng related_name đã khai báo
        serializer = ProjectPartSerializer(project_parts, many=True)
        return serializer.data