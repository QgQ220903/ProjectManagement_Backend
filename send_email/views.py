from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .serializers import SendEmailSerializer
from django.core.mail import EmailMessage
class SendEmailViewSet(viewsets.ViewSet):
    serializer_class = SendEmailSerializer

    @action(detail=False, methods=['post'], url_path='send')
    def send_email(self, request):
        serializer = SendEmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        subject = data['subject']
        message = data['message']  # HTML nội dung email
        recipient = data['recipient']

        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[recipient]
            )
            email.content_subtype = "html"  
            email.send()

            return Response({"success": "Email sent"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
