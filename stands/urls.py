from django.urls import path, include
from .views import *


app_name = 'stands'

urlpatterns = [
    path('', stands_list, name = 'stands-list'),
    path('testobjects/', include('generaltables.urls')),
    path('trials/', include('trials.urls')),
    path('calculatedtrials/', include('calculatedtrials.urls')),
]
