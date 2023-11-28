from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('about/author/', views.AtuhorAbout.as_view(), name = 'author'),
    path('about/tech/', views.TechnAbout.as_view(), name = 'tech'),
    
]


