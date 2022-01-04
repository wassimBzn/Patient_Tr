# -*- encoding: utf-8 -*-
from django.conf.urls import url

from django.urls import path, re_path
from apps.app.views import *

urlpatterns = [

    # The home page
    path('', index, name='home'),
    path('add_patient/',add_patient,name='add_patient'),
    path('view_patient/<str:patient_id>/',view_patient,name='view_patient'),
    path('update_patient/<str:patient_id>/',update_patient,name='update_patient'),
    path('delete_patient/<str:patient_id>/',delete_patient,name='delete_patient'),
    path('consultations/',consultations,name='consultations'),
    path('consultation_patient/<str:patient_id>/',consultation_patient,name='consultation_patient'),
    path('consultation_patient/<str:patient_id>/<str:action>/<str:consultation_id>/',consultation_patient,name='consultation_patient'),
    path('delete_consultation_patient/<str:patient_id>/<str:consultation_id>/',delete_consultation_patient,name='delete_consultation_patient'),
    path('delete_consultation_patient/<str:patient_id>/<str:consultation_id>/<str:source>',delete_consultation_patient,name='delete_consultation_patient'),
    path('view_consultation_patient/<str:patient_id>/<str:consultation_id>/',view_consultation_patient,name='view_consultation_patient'),
    path('global_consultation_patient/',global_consultation_patient,name='global_consultation_patient'),
    path('charts_patient/',charts_patient,name='charts_patient'),
    path('Export_excel/',Export_excel_patient,name='Export_excel'),
    path('Export_excel_patient_consultations/',Export_excel_patient_consultations,name='Export_excel_patient_consultations'),

    # Matches any html file
    # re_path(r'^.*\.*', pages, name='pages'),

]


