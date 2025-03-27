# project_part/serializers.py
from rest_framework import serializers

from .models import Role
from role_detail.serializers import RoleDetailSerializer
class RoleSerializer(serializers.ModelSerializer):
    role_details = RoleDetailSerializer(source="role_details.all", many=True)
    class Meta:
        model = Role
        fields = '__all__'