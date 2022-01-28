# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import datetime
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
GENDER_CHOICES =(
    ("Masculin", "Masculin"),
    ("Féminin", "Féminin"),
)
YES_OR_NO_CHOICES=(
    ("OUI", "OUI"),
    ("NON", "NON"),
)

STATUT_MATRIMONIAL_CHOICES=(
    ('Celibataire','Celibataire'),
    ('Mariée','Mariée'),
    ('Veuve','Veuve'),
    ('Divorcée','Divorcée'),
)
date = str(datetime.datetime.now().day) + str(datetime.datetime.now().month) + str(datetime.datetime.now().year) + str(datetime.datetime.now().hour) +  str(datetime.datetime.now().minute)+str(datetime.datetime.now().second)
date=int(date)
class Habitude(models.Model):
    id = models.AutoField(primary_key=True, default=date)
    Tabagisme = models.CharField(max_length=10 ,choices=YES_OR_NO_CHOICES)
    Nombre_de_Cigarette_par_jours = models.IntegerField(default=0)
    Alcool = models.CharField(max_length=10 ,choices=YES_OR_NO_CHOICES)
    Allergies_medicamenteuses = models.CharField(max_length=10 ,choices=YES_OR_NO_CHOICES)
    Autres= models.CharField(max_length=300)


class Antecedentes(models.Model):
    id = models.AutoField(primary_key=True, default=date)
    Medicaux = models.CharField(max_length=500,default=None)
    Chururgicaux = models.CharField(max_length=500,default=None)
    Medications_en_cours = models.CharField(max_length=500,default=None)

class Examen_phisique(models.Model):
    id = models.AutoField(primary_key=True, default=date)
    plaintes = models.CharField(max_length=500,default=None)
    Examen_Cinetique = models.CharField(max_length=500,default=None)
    Reste_de_examen_phisique = models.CharField(max_length=500,default=None)

class Examen_clinique(models.Model):
    id = models.AutoField(primary_key=True, default=date)
    Temperature = models.FloatField()
    PA = models.FloatField()
    SRO = models.FloatField(default=0, validators=PERCENTAGE_VALIDATOR)
    Poids = models.FloatField(default=1)
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
    used =models.BooleanField(default=True)

class Consultation(models.Model):
    id = models.AutoField(primary_key=True, default=date)
    Patient = models.ForeignKey(Patient,on_delete=models.PROTECT,related_name='Consultation',default=None)
    Date_de_consultation = models.DateTimeField(default=timezone.now)
    Habitude = models.ForeignKey(Habitude,on_delete=models.PROTECT,related_name='Consultation',default=None)
    Antecedentes = models.ForeignKey(Antecedentes,on_delete=models.PROTECT,related_name='Consultation',default=None)
    Examen_phisique = models.ForeignKey(Examen_phisique,on_delete=models.PROTECT,related_name='Consultation',default=None)
    Examen_clinique = models.ForeignKey(Examen_clinique,on_delete=models.PROTECT,related_name='Consultation',default=None)
    Explorations = models.CharField(max_length=500,default=None)
    Traitement = models.CharField(max_length=500,default=None)
    Evolution = models.CharField(max_length=500,default=None)
    Remarques = models.CharField(max_length=500,default=None)
    Prochaine_Rondez_vous = models.DateTimeField(default=timezone.now)
    archived= models.BooleanField(default=False)
