from django.contrib import admin

# Register your models here.
from core.models import *
from django.contrib.admin import ModelAdmin,TabularInline

class CarImageInline(TabularInline):
    model = CarImage
    extra = 5

class CarInline(ModelAdmin):
    model = Car
    extra = 1
    inlines = [CarImageInline]
    classes = ["collapse"]

    exclude = ('title',)

admin.site.register(Car,CarInline)
admin.site.register(Year)
admin.site.register(Contact)