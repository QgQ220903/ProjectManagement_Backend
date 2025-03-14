from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'  # Hoặc bạn có thể chỉ định các trường cụ thể: ['id', 'name', 'is_deleted', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] # Các trường chỉ đọc.