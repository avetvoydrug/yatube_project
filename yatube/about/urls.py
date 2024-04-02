from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('author/', views.AuthorAbout.as_view(), name = 'author'),
    path('tech/', views.TechAbout.as_view(), name = 'tech'),
    
]


