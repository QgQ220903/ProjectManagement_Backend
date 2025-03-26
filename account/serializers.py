# project_part/serializers.py
from rest_framework import serializers

from employee.serializers import EmployeeSerializer
from .models import Account,Role
from employee.models import Employee
class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'email', 'password', 'role',  'employee']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role', None)  # Lấy role từ role_id
        employee = validated_data.pop('employee', None)  # Lấy employee từ employee_id

        user = Account.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=role,  # Bổ sung role vào đây để tránh lỗi NULL
            employee= employee
        )


        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()