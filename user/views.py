from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import *
from django.http import Http404

from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView 
from django.views.generic import CreateView,TemplateView, UpdateView,View,ListView,DeleteView

from django.contrib.auth.views import LoginView
from user.forms import  *

from django.views import generic

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from user.utils import account_activation_token

from user.tasks import send_email_confirmation


USER = get_user_model()
  
  
class UserLoginView(LoginView):
    template_name = 'home.html'
    form_class = MyUserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

@login_required
def logout(request):
    django_logout(request)
    return redirect('home')


class AccountRegistrationView(generic.CreateView):
    """
        Account Register View if user is login
        Return to dashboard view
    """

    template_name = "register.html"
    form_class = BaseRegistrationForm
    model = User
    success_url = reverse_lazy("login")
    user = None

    def form_valid(self, form):
        user = form.save()
        if form.data['user_choices'] == 'User':
            user.is_active = False
        elif form.data['user_choices'] == 'Company':
            user.is_active = False
            user.is_provider_active = False
        current_site = self.request.META['HTTP_HOST']
        send_email_confirmation(user, current_site)
        print("valid")
        user.save()

        return super().form_valid(form)

class MyCarsView(LoginRequiredMixin, ListView):
    template_name = 'customer.html'
    model = Car
    

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    


    def get_context_data(self, **kwargs):
        context = super(MyCarsView, self).get_context_data(**kwargs)
        cars = Car.objects.filter(company=self.request.user)
        context['cars'] = cars
        return context


@login_required
def ProfileSettingsView(request):
    user_form = AccountUpdateModelForm(instance=request.user)
    if request.method == "POST" and 'first_name' in request.POST:
        user_form = AccountUpdateModelForm(request.POST,  request.FILES,instance=request.user)
        user_form.fields["first_name"].required = True
        user_form.fields["last_name"].required = True
        user_form.fields["phone"].required = True
        user_form.fields["address"].required = True

        if user_form.is_valid():
            print('works')
            user_form.save()
            messages.add_message(request, messages.SUCCESS, _("Your profile has been updated successfully."))

            return redirect('profile')
        else:
            return render(request, 'updateCustomer.html', {
                'user_form': user_form,
            })
    context = {
        'user_form': user_form,
    }
    return render(request, 'updateCustomer.html',context)

class ForgetPasswordView(views.PasswordResetView):
    """
        Forget password view
    """

    template_name = "activation_page_email.html" #onceden forgot.html vardi
    subject_template_name = "password_reset_subject.txt"
    email_template_name = "password_reset_email.html"
    success_url = reverse_lazy("forget-done")
    form_class = PasswordResetForm

    def get_context_data(self, **kwargs):
        context = super(ForgetPasswordView, self).get_context_data(**kwargs)
        return context
    
class ForgetPasswordDoneView(views.PasswordResetDoneView):
    """
        Forget password view
    """

    template_name = "forget-done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ForgetPasswordResetConfirmView( views.PasswordResetConfirmView):
    """
        Forget password view
    """

    template_name = "reset_password.html"#forget-confirm
    # post_reset_login = True
    success_url = reverse_lazy("forget-complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class ForgetPasswordCompleteView(views.PasswordResetCompleteView,views.TemplateView):
    """
        Forget password Complete view
    """

    template_name = "reset-password-done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class Activate(View):
    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = USER.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, USER.DoesNotExist):
            user = None
        if user.is_active:
            messages.add_message(request, messages.SUCCESS, 'Email has been confirm')
            return redirect(reverse_lazy('login'))
        elif user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Email confirmed')
            return redirect(reverse_lazy('login'))
        else:
            messages.add_message(request, messages.SUCCESS, 'Email didnot confirm')
            return redirect(reverse_lazy('/'))