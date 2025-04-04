# tasks.py
from background_task import background
from datetime import timedelta
from django.core.mail import EmailMessage
from django.conf import settings

@background 
def send_email_later(subject, message, recipient):
    try:
        print(f"Sending email to {recipient} with subject: {subject}")
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[recipient]
        )
        email.content_subtype = "html"  # Thiết lập định dạng nội dung email là HTML
        email.send()
    except Exception as e:
        print(f"Error sending email: {e}")
