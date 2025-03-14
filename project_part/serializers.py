# projects/serializers.py
from rest_framework import serializers
from .models import ProjectPart

class ProjectPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPart
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']