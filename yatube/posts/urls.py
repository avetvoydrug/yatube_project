from django.urls import path

from . import views

from .models import Group

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='main_page'),
    path('group/<slug:slug>/', views.group_posts, name='group_list')
]