from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
    def validate_email(self, value):
        if value:
            qs = Employee.objects.filter(email=value, is_deleted=False)
            # Nếu đang cập nhật, loại trừ chính instance hiện tại
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError("Email đã có người sử dụng")
        return value

    def validate_phone_number(self, value):
        if value:
            qs = Employee.objects.filter(phone_number=value, is_deleted=False)
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError("Số điện thoại đã có người sử dụng")
        return value