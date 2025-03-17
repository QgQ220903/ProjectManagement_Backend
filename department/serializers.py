from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

    def validate_departmentName(self, value):
        if not value.strip():  # Kiểm tra nếu tên phòng ban bị rỗng hoặc chỉ chứa khoảng trắng
            raise serializers.ValidationError("Tên phòng ban không được để trống.")
        return value
