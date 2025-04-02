# project_part/serializers.py
from rest_framework import serializers
from .models import Message
from file.serializers import FileSerializer
from employee.serializers import EmployeeSerializer
class MessageSerializer(serializers.ModelSerializer):
    sender = EmployeeSerializer() # Lấy email thay vì ID
    file = FileSerializer()  # Serialize file

    class Meta:
        model = Message
        fields = ['sender', 'content', 'timestamp', 'file']