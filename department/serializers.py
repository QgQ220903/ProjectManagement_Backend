from rest_framework import serializers  # Import thư viện serializers của Django REST Framework
from .models import Department  # Import model Department từ models.py của ứng dụng hiện tại
from employee.serializers import EmployeeSerializer  # Import EmployeeSerializer từ ứng dụng 'employee'
from employee.models import Employee  # Import model Employee từ ứng dụng 'employee'

class DepartmentSerializer(serializers.ModelSerializer):
    manager = EmployeeSerializer(read_only=True)  # Sử dụng EmployeeSerializer để hiển thị thông tin chi tiết của manager. read_only=True để chỉ đọc.
    employee_count = serializers.SerializerMethodField()  # 👈 Thêm dòng này
    class Meta:
        model = Department  # Liên kết serializer với model Department
        fields = '__all__'  # Sử dụng tất cả các trường của model Department

    def get_employee_count(self, obj):
        return obj.employees.filter(is_deleted=False).count()  # 👈 hoặc điều kiện phù hợp với model

    def create(self, validated_data):
        manager_id = validated_data.pop('manager', None)  # Lấy manager_id từ validated_data và loại bỏ nó
        if manager_id:  # Nếu manager_id tồn tại
            validated_data['manager'] = Employee.objects.get(pk=manager_id)  # Lấy đối tượng Employee tương ứng và gán cho manager
        return Department.objects.create(**validated_data)  # Tạo Department với validated_data đã được xử lý

    def update(self, instance, validated_data):
        manager_id = validated_data.pop('manager', None)  # Lấy manager_id từ validated_data và loại bỏ nó
        if manager_id:  # Nếu manager_id tồn tại
            validated_data['manager'] = Employee.objects.get(pk=manager_id)  # Lấy đối tượng Employee tương ứng và gán cho manager
        return super().update(instance, validated_data)  # Cập nhật Department với validated_data đã được xử lý

class DepartmentCreateUpdateSerializer(serializers.ModelSerializer):
    manager = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), allow_null=True)
    class Meta:
        model = Department
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.manager:  # Nếu có manager, thay thế ID bằng thông tin chi tiết
            data['manager'] = EmployeeSerializer(instance.manager).data
        return data
