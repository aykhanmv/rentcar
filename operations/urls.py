from django.urls import path
from operations.views import *

urlpatterns = [
    path('add-car/', AddCarView.as_view(), name='add-car'),
    path('edit-car/<int:pk>/', EditCarView.as_view(), name='edit_car'),

]