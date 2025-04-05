import django_filters
from django.db.models import Q
from .models import Produto


class ProdutoFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='Buscar')

    class Meta:
        model = Produto
        fields = ['categoria']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(nome__icontains=value) |
            Q(descricao__icontains=value) |
            Q(categoria__nome__icontains=value)
        )
