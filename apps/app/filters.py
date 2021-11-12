import django_filters

from apps.app.models import Patient


class PatientFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(field_name='nom', lookup_expr='icontains')

    class Meta:
        model = Patient
        fields = ['nom', 'date_de_naissance']