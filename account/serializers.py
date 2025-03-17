from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from role.serializers import RoleSerializer
from role.models import Role
from django.contrib.auth import get_user_model

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()  # Lồng serializer để hiển thị thông tin role

    class Meta:
        model = User
        fields = ['id', 'username', 'role']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Sai tài khoản hoặc mật khẩu")
        return user
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=True) 
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']  # Thêm role nếu cần

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        """
        Kiểm tra mật khẩu cũ có đúng không và xác nhận mật khẩu mới có khớp không.
        """
        user = self.context['request'].user  # Lấy user từ request

        # Kiểm tra mật khẩu cũ
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": "Mật khẩu cũ không chính xác."})

        # Kiểm tra mật khẩu mới và xác nhận mật khẩu mới
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"confirm_new_password": "Mật khẩu xác nhận không khớp."})

        return data

    def update_password(self):
        """
        Cập nhật mật khẩu mới cho user.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()