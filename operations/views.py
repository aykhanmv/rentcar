from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from core.models import *
from operations.forms import *
# Create your views here.
class AddCarView(LoginRequiredMixin, CreateView):
    template_name = 'graph.html'
    form_class = AddCarForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        p = form.save(commit=False)
        print(p)
        p.company = self.request.user
        print(p.company)
        p.save()
        images = self.request.FILES.getlist("more_images")
        print(images)
        for i in images:
            CarImage.objects.create(car=p, image=i)
        return super().form_valid(form)

class EditCarView(LoginRequiredMixin, UpdateView):
    template_name = 'edit_car.html'
    form_class = EditCarForm
    success_url = reverse_lazy('profile')
    model = Car

    def get_object(self):
        return Car.objects.filter(id=self.kwargs['pk']).first()
    
    def get_context_data(self, **kwargs):
        context = super(EditCarView, self).get_context_data(**kwargs)
        cars = Car.objects.filter(id=self.kwargs['pk']).first()
        context['cars'] = cars
        return context