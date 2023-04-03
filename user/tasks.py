from user.utils import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from celery import shared_task
from django.contrib.auth import get_user_model
from pytz import timezone
from datetime import *
from core.models import *

User = get_user_model()

def send_email_confirmation(user, current_site):
    subject = 'Activate Your DriveToday Account'
    message = render_to_string('account_activation_email.html', {
        'user': user,
        'domain': current_site, 
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    msg = EmailMultiAlternatives(subject=subject, body=message, from_email=settings.EMAIL_HOST_USER, to=[user.email], )
    msg.attach_alternative(message, "text/html")
    msg.send()

@shared_task
def send_mail_to_company(user):
    mail_text = render_to_string('car_mail.html',{
        'user': user,
    })
    msg = EmailMultiAlternatives(subject='Recent User Acitivity', body=mail_text, from_email=settings.EMAIL_HOST_USER, to=[user.email], )
    msg.attach_alternative(mail_text, "text/html")
    msg.send(fail_silently=True)


@shared_task
def contact_with_us(user):
    mail_text = render_to_string('car_mail.html',{
        'user': user,
    })
    msg = EmailMultiAlternatives(subject='Recent User Acitivity', body=mail_text, from_email=settings.EMAIL_HOST_USER, to=[user.email], )
    msg.attach_alternative(mail_text, "text/html")
    msg.send(fail_silently=True)
