# -*- encoding: utf-8 -*-
from django.conf.urls import url

from django.urls import path, re_path
from apps.app.views import *

urlpatterns = [

    # The home page
    path('', index, name='home'),
    path('add_patient/',add_patient,name='add_patient'),
    path('update_patient/<str:pk>/',update_patient,name='update_patient'),
    path('delete_patient/<str:pk>/',delete_patient,name='delete_patient'),
    path('charts_patient/',charts_patient,name='charts_patient'),

    # Matches any html file
   # re_path(r'^.*\.*', pages, name='pages'),

]


