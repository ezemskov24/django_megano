from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

# Login
class UserLoginView(LoginView):
    template_name = 'registration/login.jinja2'
    redirect_authenticated_user = True

# Logout
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')
