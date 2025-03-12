from rest_framework import serializers
from .models import RoleDetail  # Import model Project từ file models.py

class RoleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleDetail
        fields = '__all__'  # Hoặc liệt kê các trường cụ thể: ['id', 'name', 'isDeleted', 'createdAt', 'updatedAt']
        # Nếu bạn muốn chỉ đọc một số trường, bạn có thể dùng read_only_fields
        #read_only_fields = ['createdAt', 'updatedAt']

    def validate(self, data):
        if not data.get('roleId'):
            raise serializers.ValidationError({"roleId": "Nhóm quyền không được để trống."})
        
        if not data.get('featureId'):
            raise serializers.ValidationError({"featureId": "Chức năng không được để trống."})

        if not data.get('action') or not data['action'].strip():
            raise serializers.ValidationError({"action": "Hành động không được để trống."})

        return data