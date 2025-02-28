from rest_framework import serializers
from .models import Project  # Import model Project từ file models.py

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'  # Hoặc liệt kê các trường cụ thể: ['id', 'name', 'isDeleted', 'createdAt', 'updatedAt']
        # Nếu bạn muốn chỉ đọc một số trường, bạn có thể dùng read_only_fields
        read_only_fields = ['createdAt', 'updatedAt']

    def validate_name(self, value):
        if not value.strip():  # Kiểm tra nếu chuỗi chỉ chứa khoảng trắng hoặc rỗng
            raise serializers.ValidationError("Tên dự án không được để trống.")
        return value