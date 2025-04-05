import django_filters
from django.db.models import Q
from .models import Categoria


class CategoriaFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='Buscar')

    class Meta:
        model = Categoria
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(nome__icontains=value) |
            Q(descricao__icontains=value)
        )
