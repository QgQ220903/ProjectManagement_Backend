from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .serializers import SendEmailSerializer
from send_email.tasks import send_email_later
from datetime import datetime
import pytz
# Hàm gửi email trong nền


class SendEmailViewSet(viewsets.ViewSet):
    serializer_class = SendEmailSerializer

    @action(detail=False, methods=['post'], url_path='send')
    def send_email(self, request):
        serializer = SendEmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        subject = data['subject']
        message = data['message']
        recipient = data['recipient']
        send_at = data['send_at']  # kiểu datetime

        
        if send_at is None:
            # Gửi ngay
            send_email_later(subject, message, recipient)
            return Response({"success": "Email is being sent immediately."}, status=status.HTTP_200_OK)

        # Nếu có thời gian gửi thì tính delay
        send_at_utc = send_at.astimezone(pytz.utc)
        now = timezone.now()  # UTC
        send_at_adjusted = send_at_utc - timedelta(hours=7)  # Điều chỉnh nếu cần
        delay_seconds = int((send_at_adjusted - now).total_seconds())
        if delay_seconds <= 0:
            delay_seconds = 5  # tối thiểu 5s nếu trễ

        print(f"[Debug] Gửi sau {delay_seconds} giây (UTC now: {now}, send_at: {send_at_utc})")

        send_email_later(subject, message, recipient, schedule=delay_seconds)

        return Response({"success": f"Email will be sent at {send_at_utc}"}, status=status.HTTP_200_OK)

