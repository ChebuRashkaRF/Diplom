from django.urls import path, include
from django.contrib.auth import views
from .views import *



urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', register, name='register'),
]
