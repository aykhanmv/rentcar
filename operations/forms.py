from django import forms

from core.models import *

class AddCarForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        "multiple": True,
        "help_texts":"Maşının şəkilləri",
    }),help_text='Maşının şəkilləri')

    class Meta:
        model = Car
        fields = ('time',
                  'year_id',
                  'about',
                  'shortAbout',
                  'marka',
                  'model',
                  'topSpeed',
                  'nm',
                  'hp',
                  'seats',
                  'price',
                  'insurance',
                  'tank',
                  'more_images'
                  )
        
class EditCarForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        "multiple": True,
        "help_texts":"Maşının şəkilləri",
    }),help_text='Maşının şəkilləri')

    class Meta:
        model = Car
        fields = ('time',
                  'year_id',
                  'about',
                  'shortAbout',
                  'marka',
                  'model',
                  'topSpeed',
                  'nm',
                  'hp',
                  'seats',
                  'price',
                  'insurance',
                  'tank',
                  'more_images'
                  )