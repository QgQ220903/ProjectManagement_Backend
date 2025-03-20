# project/serializers.py
from rest_framework import serializers
from .models import Project
from project_part.serializers import ProjectPartSerializer

class ProjectDetailSerializer(serializers.ModelSerializer):
    project_parts = ProjectPartSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']