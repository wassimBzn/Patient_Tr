from django import forms
from django.forms import SelectDateWidget

from apps.app.models import *

class AddPatientForm(forms.Form):
    nom = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "nom",
                "class": "form-control"
            }

        ))

    prenom = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "prenom",
                "class": "form-control"
            }
        ))

    date_de_naissance = forms.DateField(
        widget=SelectDateWidget(years=range(1900, 2023),
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
            attrs={
                "id": "date_de_naissance",
                "class": "form-control"
            }
        ))

    lieu_de_naissance = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "lieu_de_naissance",
                "class": "form-control"
            }
        ))

    profession = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "profession",
                "class": "form-control"
            }
        ))

    adresse = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "adresse",
                "class": "form-control"
            }
        ))

    cin = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "id": "cin",
                "class": "form-control"
            }
        ))

    sexe = forms.CharField(label='sexe',
        required=True,
        widget=forms.Select(choices=GENDER_CHOICES,
            attrs={
                "id": "sexe",
                "class": "form-control"
            }
        ),

    )
    statut_matrimonial = forms.CharField(label='statut_matrimonial',
        widget=forms.Select(
            choices=STATUT_MATRIMONIAL_CHOICES,
            attrs={
                "id": "statut_matrimonial",
                "class": "form-control"
            }
        ))

    telephone = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "id": "telephone",
                "class": "form-control"
            }
        ))


    class Meta:
        model = Patient
        fields = ("Nom","Prenom","Date_de_naissance","Lieu_de_naissance","Profession","Adresse","Cin","Sexe","Statut_matrimonial","Telephone")
