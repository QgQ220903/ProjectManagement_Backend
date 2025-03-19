from rest_framework import serializers  # Import thư viện serializers của Django REST Framework
from .models import TaskAssignment  # Import model TaskAssignment từ models.py của ứng dụng hiện tại
from employee.serializers import EmployeeSerializer  # Import EmployeeSerializer từ ứng dụng 'employee'
from task.serializers import TaskSerializer  # Import TaskSerializer từ ứng dụng 'task'

class TaskAssignmentSerializer(serializers.ModelSerializer):
    """
    Serializer để hiển thị thông tin chi tiết của TaskAssignment, bao gồm cả thông tin chi tiết của employee và task.
    """
    employee = EmployeeSerializer(read_only=True)  # Sử dụng EmployeeSerializer để hiển thị thông tin chi tiết của employee. read_only=True để chỉ đọc.
    task = TaskSerializer(read_only=True)  # Sử dụng TaskSerializer để hiển thị thông tin chi tiết của task. read_only=True để chỉ đọc.

    class Meta:
        """
        Định nghĩa metadata cho TaskAssignmentSerializer.
        """
        model = TaskAssignment  # Liên kết serializer với model TaskAssignment
        fields = '__all__'  # Sử dụng tất cả các trường của model TaskAssignment

class TaskAssignmentCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer để tạo hoặc cập nhật TaskAssignment, sử dụng PrimaryKeyRelatedField cho employee và task.
    """
    class Meta:
        """
        Định nghĩa metadata cho TaskAssignmentCreateUpdateSerializer.
        """
        model = TaskAssignment  # Liên kết serializer với model TaskAssignment
        fields = '__all__'  # Sử dụng tất cả các trường của model TaskAssignment