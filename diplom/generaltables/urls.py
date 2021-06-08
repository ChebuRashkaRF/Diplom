from django.urls import path, include
from .views import *

urlpatterns = [
    path('', testobjects_list, name = 'testobjects-list'),

]
