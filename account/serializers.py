from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from role.serializers import RoleSerializer

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
