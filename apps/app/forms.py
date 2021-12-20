from django import forms
from django.forms import SelectDateWidget
from django.utils import timezone
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
        ),initial=timezone.now())

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
class AddExamen_cliniqueForm(forms.Form):
    Temperature = forms.FloatField(required=True, max_value=70, min_value=20,
                                widget=forms.NumberInput(attrs={'id': 'Temperature',
                                                                "class": "form-control",
                                                                'step': "0.01"}))
    PA = forms.FloatField(required=True,
                                   widget=forms.NumberInput(attrs={'id': 'PA',
                                                                   "class": "form-control",
                                                                   'step': "0.01"}))
    SRO = forms.FloatField(required=True,
                                   widget=forms.NumberInput(attrs={'id': 'SRO',
                                                                   "class": "form-control",
                                                                   'step': "0.01"}))
    Poids = forms.FloatField(required=True,
                                   widget=forms.NumberInput(attrs={'id': 'Poids',
                                                                   "class": "form-control",
                                                                   'step': "0.01"}))
    Taille = forms.FloatField(required=True,
                                   widget=forms.NumberInput(attrs={'id': 'Taille',
                                                                   "class": "form-control",
                                                                   'step': "0.01"}))
    RC = forms.FloatField(required=True,
                                   widget=forms.NumberInput(attrs={'id': 'RC',
                                                                   "class": "form-control",
                                                                   'step': "0.01"}))

    Reste_de_examen_clinique = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "Reste_de_examen_clinique",
                "class": "form-control"
            }
        ))
    class Meta:
        model = Examen_clinique
        fields = ("Temperature","PA","SRO","Poids","Taille","RC","Reste_de_examen_clinique")
class AddExamen_phisiqueForm(forms.Form):

    plaintes = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "plaintes",
                "class": "form-control"
            }
        ))
    Examen_Cinetique = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "Examen_Cinetique",
                "class": "form-control"
            }
        ))
    Reste_de_examen_phisique = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "Reste_de_examen_phisique",
                "class": "form-control"
            }
        ))
    class Meta:
        model = Examen_phisique
        fields = ("plaintes","Examen_Cinetique","Reste_de_examen_phisique")
class AddAntecedentesForm(forms.Form):

    Medicaux = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "Medicaux",
                "class": "form-control"
            }
        ))
    Chururgicaux = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "Chururgicaux",
                "class": "form-control"
            }
        ))
    Medications_en_cours = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "Medications_en_cours",
                "class": "form-control"
            }
        ))
    class Meta:
        model = Antecedentes
        fields = ("Medicaux","Chururgicaux","Medications_en_cours")

class AddHabitudeForm(forms.Form):
    Tabagisme = forms.CharField(label='Tabagisme',
                                         widget=forms.Select(
                                             choices=YES_OR_NO_CHOICES,
                                             attrs={
                                                 "id": "Tabagisme",
                                                 "class": "form-control"
                                             }
                                         ))

    Nombre_de_Cigarette_par_jours = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "id": "Nombre_de_Cigarette_par_jours",
                "class": "form-control"
            }
        ))
    Alcool = forms.CharField(label='Alcool',
                                widget=forms.Select(
                                    choices=YES_OR_NO_CHOICES,
                                    attrs={
                                        "id": "Alcool",
                                        "class": "form-control"
                                    }
                                ))

    Allergies_medicamenteuses = forms.CharField(label='Allergies_medicamenteuses',
                             widget=forms.Select(
                                 choices=YES_OR_NO_CHOICES,
                                 attrs={
                                     "id": "Allergies_medicamenteuses",
                                     "class": "form-control"
                                 }
                             ))
    Autres = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "Autres",
                "class": "form-control"
            }
        ))
    class Meta:
        model = Habitude
        fields = ("Tabagisme","Nombre_de_Cigarette_par_jours","Alcool","Allergies_medicamenteuses","Autres")
class AddConsultationForm(forms.Form):
    Date_de_consultation = forms.DateField(
        widget=SelectDateWidget(years=range(2000, 2030),
                                empty_label=("Choose Year", "Choose Month", "Choose Day"),
                                attrs={
                                    "id": "Date_de_consultation",
                                    "class": "form-control"
                                },
                                ),initial=timezone.now())
    Explorations = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "Explorations",
                "class": "form-control"
            }
        ))
    Traitement = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "Traitement",
                "class": "form-control"
            }
        ))
    Evolution = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "Evolution",
                "class": "form-control"
            }
        ))
    Remarques = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "Remarques",
                "class": "form-control"
            }
        ))

    Prochaine_Rondez_vous = forms.DateField(
        widget=SelectDateWidget(years=range(2000, 2050),
                                empty_label=("Choose Year", "Choose Month", "Choose Day"),
                                attrs={
                                    "id": "Prochaine_Rondez_vous",
                                    "class": "form-control"
                                },
                                ),initial=timezone.now())


    class Meta:
        model = Consultation
        fields = ("Date_de_consultation","Explorations","Traitement","Evolution","Remarques","Prochaine_Rondez_vous")