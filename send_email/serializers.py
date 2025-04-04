# serializers.py
from rest_framework import serializers

class SendEmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField(style={'base_template': 'textarea.html'}, allow_blank=False)
    recipient = serializers.EmailField()
