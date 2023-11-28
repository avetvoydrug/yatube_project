from django.shortcuts import render
from django.views.generic import CreateView
# Позволяет получить урлы по параметрам патч()
from django.urls import reverse_lazy
from .forms import CreationForm
from django.contrib.auth.views import (PasswordChangeView)
# Create your views here.
class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:main_page')
    template_name = 'users/signup.html'


