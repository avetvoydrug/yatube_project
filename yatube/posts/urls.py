from django.urls import path, include

from . import views
from rest_framework.routers import SimpleRouter

app_name = 'posts'

router = SimpleRouter()
router.register('posts', views.PostViewSet)

urlpatterns = [
    path('', views.index, name='main_page'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    # path('create/', views.post_create, name='post_create'),
    path('create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:post_id>/comment', views.add_comment, name='add_comment'),
    path('api/v1/', include(router.urls)),
    path('api/v2/auth/', include('djoser.urls')),
    path('api/v2/auth/', include('djoser.urls.jwt')), 
]