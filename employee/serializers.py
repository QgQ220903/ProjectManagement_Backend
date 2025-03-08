from rest_framework import serializers
from .models import Employee, Department

class EmployeeSerializer(serializers.ModelSerializer):
    departmentID = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source='department'
    )

    class Meta:
        model = Employee
        fields = ['id', 'positionName', 'employeeName', 'employeePhone', 'employeeEmail', 'status', 'departmentID']
