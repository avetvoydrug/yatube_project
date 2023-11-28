from django.contrib.auth.views import (LoginView, 
                                       LogoutView, 
                                       PasswordChangeView, 
                                       PasswordChangeDoneView,
                                       PasswordResetView, 
                                       PasswordResetDoneView, 
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView
                                       )
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('logout/',
         LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(#pass_change#
        'password_change/', PasswordChangeView.as_view(
            template_name='users/password_change_form.html'),
        name='password_change'
    ),
    path(#change_done#
        'password_change/done/', PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'),
        name='password_change_done'
    ),
    path(#pass_reset#
        'password_reset/', PasswordResetView.as_view(
            template_name='users/password_reset_form.html'),
        name='password_reset_form'
    ),
    path(#reset_link_sent#
        'password_reset/done/', PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(#reset_email#
        'reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(#reset_done#
        'reset/done/', PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'),
        name='password_reset_complete'
    )
]