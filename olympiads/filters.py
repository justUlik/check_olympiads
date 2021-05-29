from .models import Olympiad
import django_filters

class OlympiadFilter(django_filters.FilterSet):
    class Meta:
        model = Olympiad
        fields = ['subject', 'rank']
