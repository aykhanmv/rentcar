
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from celery import shared_task
from django.contrib.auth import get_user_model
from pytz import timezone
from datetime import *
from core.models import *

User = get_user_model()

@shared_task
def contact_with_us(car):
    contact = Contact.objects.filter(car=car).first()
    car = Car.objects.filter(id=car.id).first()
    mail_text = render_to_string('car_contact.html',{
        'contact': contact,
        'car': car,
    })
    msg = EmailMultiAlternatives(subject='New Contact Mail', body=mail_text, from_email=settings.EMAIL_HOST_USER, to=[car.company.email], )
    msg.attach_alternative(mail_text, "text/html")
    msg.send(fail_silently=True)
