from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import signup_view, home, PasswordResetView, password_reset, password_change, send_email
from . import views

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', home, name="home"),
   
    # password change
    path('password_change/', auth_views.PasswordResetView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordResetDoneView.as_view(), name='password_change_done'),
    path('change/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_change_confirm'),
    path('change/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_change_complete'),  

    path('password_reset/', password_reset, name='password_reset'),

    path('send_email/', views.send_email, name='send_email'),
]