from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.
class AtuhorAbout(TemplateView):
    template_name = 'about/author.html'

class TechnAbout(TemplateView):
    template_name = 'about/tech.html'