from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.
class AuthorAbout(TemplateView):
    template_name = 'about/author.html'

class TechAbout(TemplateView):
    template_name = 'about/tech.html'