from django.urls import path
from core.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('car-detail/<int:pk>/', CarDetail.as_view(), name='car_detail'),
    path("car/book/<int:pk>/", BookCarView.as_view(), name="book_car"),
    path('loadForm/', loadForm, name='ajax_load'),
    path('infoGenerated/', loadData, name='infoGenerated'),

]