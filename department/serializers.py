from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        extra_kwargs = {
            'managerID': {'allow_null': True, 'required': False}  # Cho phép managerID null
        }

    def validate_departmentName(self, value):
        if not value.strip():
            raise serializers.ValidationError("Tên phòng ban không được để trống.")
        return value
