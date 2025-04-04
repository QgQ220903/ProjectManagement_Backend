from rest_framework import serializers
from datetime import datetime, timedelta
from django.utils import timezone
import pytz
class SendEmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField(style={'base_template': 'textarea.html'}, allow_blank=False)
    recipient = serializers.EmailField()
    send_at = serializers.DateTimeField(required=False,
    allow_null=True,)

    # def validate_send_at(self, value):
    #     # Chuyển thời gian thành UTC+7 (Asia/Ho_Chi_Minh)
    #     vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')

    #     # Nếu send_at không có múi giờ (naive), chúng ta sẽ gán múi giờ UTC+7
    #     if value.tzinfo is None:
    #         value = vietnam_tz.localize(value)
    #     else:
    #         # Nếu send_at đã có múi giờ, chúng ta sẽ chuyển nó sang UTC+7
    #         value = value.astimezone(vietnam_tz)

    #     # Kiểm tra nếu thời gian gửi quá sớm
    #     if value <= timezone.now() + timedelta(minutes=3):
    #         raise serializers.ValidationError("Send time must be at least 3 minutes from now.")
        
    #     return value 
