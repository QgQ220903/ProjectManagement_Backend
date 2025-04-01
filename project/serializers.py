from rest_framework import serializers
from .models import Project
from project_part.serializers import ProjectPartSerializer

class ProjectDetailSerializer(serializers.ModelSerializer):
    project_parts = ProjectPartSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'is_deleted', 
            'created_at', 'updated_at', 
            'project_parts'  # Đảm bảo có tất cả các field cần thiết
        ]
        read_only_fields = ['created_at', 'updated_at']