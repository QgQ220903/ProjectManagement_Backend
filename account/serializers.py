# project_part/serializers.py
from rest_framework import serializers

from employee.serializers import EmployeeSerializer
from .models import Account,Role
from employee.models import Employee
from role.serializers import RoleSerializer
from employee.serializers import EmployeeSerializer
class AccountSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)  # Hiển thị thông tin chi tiết role
    employee = EmployeeSerializer(read_only=True)  # Hiển thị thông tin chi tiết employee
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role', write_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), source='employee', write_only=True, allow_null=True)
    class Meta:
        model = Account
        fields = ['id', 'email', 'password', 'role','role_id',  'employee','employee_id']
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
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])  # Dùng set_password()
            validated_data.pop('password')
        return super().update(instance, validated_data)
    def to_representation(self, instance):
        """
        Ghi đè to_representation để hiển thị đầy đủ thông tin role và employee khi GET hoặc POST.
        """
        data = super().to_representation(instance)
        if instance.role:
            data['role'] = RoleSerializer(instance.role).data  # Hiển thị chi tiết role
        if instance.employee:
            data['employee'] = EmployeeSerializer(instance.employee).data  # Hiển thị chi tiết employee
        return data
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class UpdateSerializer(serializers.Serializer):
    password = serializers.CharField(required=False, write_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role', write_only=True, required=False)

    def update(self, instance, validated_data):
        # Cập nhật mật khẩu nếu có
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        # Cập nhật role nếu có
        if 'role' in validated_data:
            instance.role = validated_data['role']

        instance.save()
        return instance
