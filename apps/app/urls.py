# -*- encoding: utf-8 -*-
from django.conf.urls import url

from django.urls import path, re_path
from apps.app.views import *

urlpatterns = [

    # The home page
    path('', index, name='home'),
    path('add_patient/',add_patient,name='add_patient'),
    # Matches any html file
   # re_path(r'^.*\.*', pages, name='pages'),

]


