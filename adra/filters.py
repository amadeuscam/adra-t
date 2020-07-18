import django_filters
from adra.models import Alimentos


class AlimentosFilters(django_filters.FilterSet):
    class Meta:
        model = Alimentos
        # fields = ['fecha_recogida']
        fields = {
            'created_at': ['year', 'month','day']
        }
