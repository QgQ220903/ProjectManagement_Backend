from rest_framework import serializers
from .models import Account  # Import model Project từ file models.py

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'  # Hoặc liệt kê các trường cụ thể: ['id', 'employee_id', 'role_id', 'username', 'password', 'status]

    def validate_username(self, value):
        """ Kiểm tra username không rỗng và không chứa khoảng trắng """
        if not value.strip():  
            raise serializers.ValidationError("Tên người dùng không được để trống.")
        if " " in value:  
            raise serializers.ValidationError("Tên người dùng không được chứa khoảng trắng.")
        return value

    def validate_password(self, value):
        """ Kiểm tra password không rỗng và không chứa khoảng trắng """
        if not value.strip():  
            raise serializers.ValidationError("Mật khẩu không được để trống.")
        if " " in value:  
            raise serializers.ValidationError("Mật khẩu không được chứa khoảng trắng.")
        return value