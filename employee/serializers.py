from rest_framework import serializers
from .models import Employee, Department

class EmployeeSerializer(serializers.ModelSerializer):
    departmentID = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source='department'
    )

    class Meta:
        model = Employee
        fields = ['id', 'positionName', 'employeeName', 'employeePhone', 'employeeEmail', 'status', 'departmentID']
    def validate_employeeName(self, value):
        if not value.strip():
            raise serializers.ValidationError("Tên nhân viên không được để trống.")
        return value

    def validate_employeeEmail(self, value):
        if "@" not in value:
            raise serializers.ValidationError("Email không hợp lệ.")
        return value