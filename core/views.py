from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView,View,CreateView
from django.urls import reverse_lazy
from core.models import *
from django.contrib.auth.mixins import LoginRequiredMixin

from user.forms import *
from user.tasks import send_mail_to_company
from core.tasks import contact_with_us
from django.contrib.auth import get_user_model
from core.forms import ContactForm
# Create your views here.
USER = get_user_model()

class HomeView(ListView):
    template_name = 'home.html'
    model = Car

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        cars = Car.objects.all()[0:4]
        carsList = Car.objects.all()
        year = Year.objects.all()
        context['cars'] = cars
        context['year'] = year
        context['carsList'] = carsList
        return context

class CarDetail(DetailView,CreateView):
    model = Car
    template_name = "car.html"
    form_class = ContactForm
    # context_object_name = "cars"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        result = super().form_valid(form)
        car = get_object_or_404(Car, id=self.kwargs['pk'])
        contact = form.save(commit=False)
        contact.car = car
        contact.save()
        contact_with_us(car)
        return result
    
    def get_context_data(self, **kwargs):
        context = super(CarDetail, self).get_context_data(**kwargs)
        context["cars"] = Car.objects.filter(pk=self.kwargs.get('pk'))
        return context
    
    
class BookCarView(LoginRequiredMixin, View):
    model = User
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Car, id=self.kwargs['pk'])
        user = User.objects.filter(cars=obj).first()
        # print(user.email)
        obj.is_booked = not obj.is_booked

        if obj.is_booked:
            obj.booker = request.user
        else:
            obj.booker = None

        obj.save()
        send_mail_to_company(user)
        return redirect(reverse_lazy('car_detail', kwargs={"pk": obj.id}))
    
def loadData(request):
    current   = request.user
    yearData  = request.POST['carYear']
    modelData = request.POST['carModel']
    print(current)
    print(modelData)
    if not modelData and not yearData:
        carDatabase = Car.objects.all()[4:]
    elif not modelData:
        carDatabase = Car.objects.filter(year_id=yearData)
    else:
        carDatabase = Car.objects.filter(year_id=yearData, id=modelData )
    
    context={'modelData':modelData,
    'yearData':yearData,
    'carDatabase':carDatabase,
    'current':current }
    return render(request,'infoGenerated.html',context)


def loadForm(request):
    year_id = request.GET.get('carYear')
    selectedCar = Car.objects.filter(year_id=year_id).order_by('model')

    context={'selectedCar':selectedCar}
    return render(request,'dropList.html',context)