# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import datetime
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
GENDER_CHOICES =(
    ("Male", "Masculin"),
    ("Female", "Féminin"),
)
YES_OR_NO_CHOICES=(
    ("YES", "OUI"),
    ("NO", "NON"),
)

STATUT_MATRIMONIAL_CHOICES=(
    ('celibataire','célibataire'),
    ('mariee','Mariée'),
    ('veuve','Veuve'),
    ('divorcee','divorcée'),
)

class Habitude(models.Model):
    Tabagisme = models.CharField(max_length=10 ,choices=YES_OR_NO_CHOICES)
    Nombre_de_Cigarette_par_jours = models.IntegerField(primary_key=True,default=0)
    Alcool = models.CharField(max_length=10 ,choices=YES_OR_NO_CHOICES)
    Allergies_medicamenteuses = models.CharField(max_length=10 ,choices=YES_OR_NO_CHOICES)
    Autres= models.CharField(max_length=300)


class Antecedentes(models.Model):
    Medicaux= models.CharField(max_length=500,default=None)
    Chururgicaux= models.CharField(max_length=500,default=None)
    Medications_en_cours= models.CharField(max_length=500,default=None)

class Examen_phisique(models.Model):
    plaintes = models.CharField(max_length=500,default=None)
    Examen_Cinetique= models.CharField(max_length=500,default=None)
    Reste_de_examen_phisique= models.CharField(max_length=500,default=None)

class Examen_clinique(models.Model):
    Temperature = models.FloatField()
    PA = models.FloatField()
    SRO = models.FloatField(default=0, validators=PERCENTAGE_VALIDATOR)
    poids = models.FloatField(default=1)
    Taille = models.FloatField(default=1)
    RC = models.IntegerField(default=70)
    Reste_de_examen_clinique = models.CharField(max_length=500)


class Patient(models.Model):
    Nom = models.CharField(max_length=200)
    Prenom = models.CharField(max_length=200)
    Date_de_naissance = models.DateField()
    Lieu_de_naissance = models.CharField(max_length=200)
    Profession = models.CharField(max_length=200)
    Adresse = models.CharField(max_length=200)
    Cin = models.IntegerField(primary_key= True)
    Sexe = models.CharField(max_length=200,choices=GENDER_CHOICES)
    Statut_matrimonial = models.CharField(max_length=200,choices=STATUT_MATRIMONIAL_CHOICES)
    Telephone = models.IntegerField()

class Consultation(models.Model):
    Patient = models.ForeignKey(Patient,on_delete=models.PROTECT,related_name='Consultation',default=None)
    Date_de_consultation = models.DateTimeField(default=datetime.datetime.now())
    Habitude = models.ForeignKey(Habitude,on_delete=models.PROTECT,related_name='Patient',default=None)
    Antecedentes = models.ForeignKey(Antecedentes,on_delete=models.PROTECT,related_name='Patient',default=None)
    Examen_phisique = models.ForeignKey(Examen_phisique,on_delete=models.PROTECT,related_name='Consultation',default=None)
    Examen_clinique = models.ForeignKey(Examen_clinique,on_delete=models.PROTECT,related_name='Consultation',default=None)
    Explorations = models.CharField(max_length=500,default=None)
    Traitement = models.CharField(max_length=500,default=None)
    Evolution = models.CharField(max_length=500,default=None)
    Remarques = models.CharField(max_length=500,default=None)
    Prochaine_Rondez_vous = models.DateTimeField(default=datetime.datetime.now())
