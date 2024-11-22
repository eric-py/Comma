from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm

User = get_user_model()

# Create your views here.

class UserLoginView(LoginView):
    template_name = 'account/auth.html'
    form_class = AuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Comma | صفحه ورود'
        context['active'] = 'login'
        return context

class UserRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'account/auth.html'
    success_url = reverse_lazy('account:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Comma | ثبت نام'
        context['active'] = 'register'
        return context