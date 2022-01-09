# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from apps.app.models import *

admin.site.register(Patient)
admin.site.register(Antecedentes)
admin.site.register(Consultation)
admin.site.register(Examen_phisique)
admin.site.register(Examen_clinique)
admin.site.register(Habitude)
