from django import forms
from core.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            'name',
            'email',
            'phone',
            'message',
        )
        labels = {
            'name': 'Your Name',
            'email': 'Email',
            'phone': 'Phone number',
            'message': 'Message',
        }
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
