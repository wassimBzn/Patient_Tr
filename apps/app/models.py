# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    date_de_naissance = models.DateField()
    lieu_de_naissance = models.CharField(max_length=200)
    profession = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    cin = models.IntegerField()
    statut_matrimonial = models.CharField(max_length=200)
    telephone = models.IntegerField(primary_key = True)
    habitude = models.CharField(max_length=400)
    antecedentes= models.CharField(max_length=400)
    medication_en_cours = models.CharField(max_length=400)
    plaintes = models.CharField(max_length=400)
    reste_de_examen = models.CharField(max_length=400)
    T = models.BooleanField()
    PA = models.BooleanField()
    Slo = models.BooleanField()
    RC = models.BooleanField()
    explorations = models.CharField(max_length=400)
    traitement = models.CharField(max_length=400)
    evolution = models.CharField(max_length=400)
