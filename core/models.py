from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Year(models.Model):
    name = models.CharField(max_length=4,unique=True)

    def __str__(self):
        return "{}".format(self.name)


class Car(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cars')
    year_id    = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
    time       = models.FloatField(null=True,blank=True)
    about      = models.TextField(max_length=355,null=True, blank=True)
    shortAbout = models.CharField(max_length=70,null=True, blank=True)
    marka      = models.CharField(max_length=50,null=True, blank=True)
    model      = models.CharField(max_length=70,null=True, blank=True)
    topSpeed   = models.IntegerField(null=True,blank=True)
    nm         = models.IntegerField(null=True,blank=True)
    hp         = models.IntegerField(null=True,blank=True)
    seats      = models.IntegerField(null=True,blank=True)
    price      = models.CharField(max_length=10,null=True,blank=True)
    insurance  = models.IntegerField(null=True,blank=True)
    tank       = models.IntegerField(null=True,blank=True)
    is_booked = models.BooleanField(default=False)
    booker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='booked_cars')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.marka} {self.model}'
    
    
class CarImage(models.Model):
    car = models.ForeignKey('Car',related_name="car_images", on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    is_main = models.BooleanField('Main picture', default=False, help_text="Assign one of the pictures as a main one.") 

    def __str__(self):
        return "{}".format(self.image.url)

    class Meta:
        verbose_name = 'Car image'
        verbose_name_plural = 'Car images'

class Contact(models.Model):
    car = models.ForeignKey('Car',related_name="car_contacts", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=40)
    phone = models.CharField(max_length=20)
    message = models.TextField()

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.name
