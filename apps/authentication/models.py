# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
GENDER_CHOICES =(
    ("Masculin", "Masculin"),
    ("Féminin", "Féminin"),
)
Roles=(
    ("Administrateur", "Administrateur"),
    ("Secrétaire", "Secrétaire"),
)

STATUT_MATRIMONIAL_CHOICES=(
    ('Celibataire','Celibataire'),
    ('Mariée','Mariée'),
    ('Veuve','Veuve'),
    ('Divorcée','Divorcée'),
)
# Create your models here.
class Employee(models.Model):
    Nom = models.CharField(max_length=200)
    Prenom = models.CharField(max_length=200)
    Username = models.CharField(max_length=200)
    Email = models.CharField(max_length=200)
    Date_de_naissance = models.DateField()
    Lieu_de_naissance = models.CharField(max_length=200)
    Role = models.CharField(max_length=200,choices=Roles)
    Adresse = models.CharField(max_length=200)
    Cin = models.IntegerField(primary_key= True)
    Sexe = models.CharField(max_length=200,choices=GENDER_CHOICES)
    Statut_matrimonial = models.CharField(max_length=200,choices=STATUT_MATRIMONIAL_CHOICES)
    Telephone = models.IntegerField()