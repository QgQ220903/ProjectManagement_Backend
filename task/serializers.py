# task/serializers.py
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def update(self, instance, validated_data):
        task_status = validated_data.get('task_status', instance.task_status)
        instance = super().update(instance, validated_data)
        
        # Gọi update_completion ngay lập tức khi task_status thay đổi
        if 'task_status' in validated_data:
            instance.update_completion()
            
        return instance

class TaskStatisticsFilterSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField(required=True)
    end_date = serializers.DateTimeField(required=True)