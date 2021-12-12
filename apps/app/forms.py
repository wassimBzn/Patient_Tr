from django import forms
from django.forms import SelectDateWidget

from apps.app.models import *

GENDER_CHOICES =(
    ("Male", "Masculine"),
    ("Female", "Feminine"),
)

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

    sexe = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "id": "statut_matrimonial",
                "class": "form-control"
            }
        ),
        choices=GENDER_CHOICES,
    )
    statut_matrimonial = forms.CharField(
        widget=forms.TextInput(
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

    tabagisme = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "tabagisme",
                "class": "form-control"
            }
        ))

    antecedentes = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "antecedentes",
                "class": "form-control"
            }
        ))

    medication_en_cours = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "medication_en_cours",
                "class": "form-control"
            }
        ))

    plaintes = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "plaintes",
                "class": "form-control"
            }
        ))


    Temperature = forms.FloatField(required=False,
        widget=forms.NumberInput(
            attrs={
                "id": "Temperature",
                "class": "form-control"
            }
        ))

    PA = forms.FloatField(required=False,
        widget=forms.NumberInput(
            attrs={
                "id": "PA",
                "class": "form-control"
            }
        ))

    Poids = forms.FloatField(required=False,
        widget=forms.NumberInput(
            attrs={
                "id": "Poids",
                "class": "form-control"
            }
        ))


    Taille = forms.FloatField(required=False,
        widget=forms.NumberInput(
            attrs={
                "id": "Taille",
                "class": "form-control"
            }
        ))
    SRO = forms.FloatField(required=False,
        widget=forms.NumberInput(
            attrs={
                "id": "SRO",
                "class": "form-control"
            }
        ))

    RC = forms.FloatField(required=False,
        widget=forms.NumberInput(
            attrs={
                "id": "RC",
                "class": "form-control"
            }
        ))
    reste_de_examen_clinique = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "reste_de_examen_clinique",
                "class": "form-control"
            }
        ))

    explorations = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "explorations",
                "class": "form-control"
            }
        ))

    traitement = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "traitement",
                "class": "form-control"
            }
        ))

    evolution = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "evolution",
                "class": "form-control"
            }
        ))

    class Meta:
        model = Patient
        fields = (
        "nom", "prenom", "date_de_naissance", "lieu_de_naissance", "profession", "adresse", "cin", "statut_matrimonial",
        "telephone", "habitude", "antecedentes", "medication_en_cours", "plaintes", "reste_de_examen", "T", "PA", "Slo",
        "RC", "explorations", "traitement", "evolution")
