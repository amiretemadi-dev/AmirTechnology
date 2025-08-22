from django.core.mail import send_mail
from django.conf import settings
from .models import VerificationCode
from django.utils import timezone


def send_verification_email(email, code):
    subject = 'Amir-Tec Verification Code'
    message = f'Your verification code is: {code}\nThis code is valid for 10 minutes.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
