import django_filters

from apps.app.models import Patient


class PatientFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(field_name='Nom', lookup_expr='icontains')
    prenom = django_filters.CharFilter(field_name='Prenom', lookup_expr='icontains')
    cin = django_filters.NumberFilter(field_name='Cin', lookup_expr='icontains')

    class Meta:
        model = Patient
        fields = ['Cin', 'Nom', 'Prenom', 'Date_de_naissance',]