# project_part/serializers.py
from rest_framework import serializers

from .models import RoleDetail
class RoleDetailSerializer(serializers.ModelSerializer):
    # role_name = serializers.CharField(source="role.name", read_only=True)
    # feature_name = serializers.CharField(source="feature.name", read_only=True)
    class Meta:
        model = RoleDetail
        fields = '__all__'