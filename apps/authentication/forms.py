# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import SelectDateWidget
from django.utils import timezone
from apps.authentication.models import *


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))

class AddEmployeeForm(forms.Form):
    nom = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "nom",
                "id": "nom",
                "class": "form-control"
            }

        ))

    prenom = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "prenom",
                "id": "prenom",
                "class": "form-control"
            }
        ))

    date_de_naissance = forms.DateField(
        widget=SelectDateWidget(years=range(1900, 2023),
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
            attrs={
                "placeholder": "date_de_naissance",
                "id": "date_de_naissance",
                "class": "form-control"
            }
        ),initial=timezone.now())

    lieu_de_naissance = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "lieu_de_naissance",
                "id": "lieu_de_naissance",
                "class": "form-control"
            }
        ))

    role = forms.CharField(label='role',
        required=True,
        widget=forms.Select(choices=Roles,
            attrs={
                "placeholder": "Role",
                "id": "Role",
                "class": "form-control"
            }

        ))

    adresse = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "adresse",
                "id": "adresse",
                "class": "form-control"
            }
        ))

    cin = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "cin",
                "id": "cin",
                "class": "form-control"
            }
        ))

    sexe = forms.CharField(label='sexe',
        required=True,
        widget=forms.Select(choices=GENDER_CHOICES,
            attrs={
                "placeholder": "sexe",
                "id": "sexe",
                "class": "form-control"
            }
        ),

    )
    statut_matrimonial = forms.CharField(label='statut_matrimonial',
        widget=forms.Select(
            choices=STATUT_MATRIMONIAL_CHOICES,
            attrs={
                "placeholder": "statut_matrimonial",
                "id": "statut_matrimonial",
                "class": "form-control"
            }
        ))

    telephone = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "placeholder": "telephone",
                "id": "telephone",
                "class": "form-control"
            }
        ))


    class Meta:
        model = Employee
        fields = ("Nom","Prenom","Date_de_naissance","Lieu_de_naissance","Role","Adresse","Cin","Sexe","Statut_matrimonial","Telephone")

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
