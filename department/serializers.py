from rest_framework import serializers  # Import thư viện serializers của Django REST Framework
from .models import Department  # Import model Department từ models.py của ứng dụng hiện tại
from employee.serializers import EmployeeSerializer  # Import EmployeeSerializer từ ứng dụng 'employee'
from employee.models import Employee  # Import model Employee từ ứng dụng 'employee'

class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer để hiển thị thông tin chi tiết của Department, bao gồm cả thông tin chi tiết của manager.
    """
    manager = EmployeeSerializer(read_only=True)  # Sử dụng EmployeeSerializer để hiển thị thông tin chi tiết của manager. read_only=True để chỉ đọc.

    class Meta:
        """
        Định nghĩa metadata cho DepartmentSerializer.
        """
        model = Department  # Liên kết serializer với model Department
        fields = '__all__'  # Sử dụng tất cả các trường của model Department

    def create(self, validated_data):
        """
        Ghi đè phương thức create để xử lý việc tạo Department với manager.
        """
        manager_id = validated_data.pop('manager', None)  # Lấy manager_id từ validated_data và loại bỏ nó
        if manager_id:  # Nếu manager_id tồn tại
            validated_data['manager'] = Employee.objects.get(pk=manager_id)  # Lấy đối tượng Employee tương ứng và gán cho manager
        return Department.objects.create(**validated_data)  # Tạo Department với validated_data đã được xử lý

    def update(self, instance, validated_data):
        """
        Ghi đè phương thức update để xử lý việc cập nhật Department với manager.
        """
        manager_id = validated_data.pop('manager', None)  # Lấy manager_id từ validated_data và loại bỏ nó
        if manager_id:  # Nếu manager_id tồn tại
            validated_data['manager'] = Employee.objects.get(pk=manager_id)  # Lấy đối tượng Employee tương ứng và gán cho manager
        return super().update(instance, validated_data)  # Cập nhật Department với validated_data đã được xử lý

class DepartmentCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer để tạo hoặc cập nhật Department, sử dụng PrimaryKeyRelatedField cho manager.
    """
    manager = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), allow_null=True)  # Sử dụng PrimaryKeyRelatedField để cho phép chọn manager bằng ID. allow_null=True để cho phép manager là null.

    class Meta:
        """
        Định nghĩa metadata cho DepartmentCreateUpdateSerializer.
        """
        model = Department  # Liên kết serializer với model Department
        fields = '__all__'  # Sử dụng tất cả các trường của model Department