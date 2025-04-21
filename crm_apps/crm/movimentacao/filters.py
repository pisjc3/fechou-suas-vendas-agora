import django_filters
from django.db.models import Q
from .models import Movimentacao


class MovimentacaoFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='Buscar')

    class Meta:
        model = Movimentacao
        fields = ['produto', 'quantidade', 'tipo', 'preco_unitario',
                  'cliente', 'empresa', 'novo_preco_custo', 'novo_preco_venda']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(produto__nome__icontains=value) |
            Q(quantidade__icontains=value) |
            Q(tipo__icontains=value) |
            Q(preco_unitario__icontains=value) |
            Q(cliente__nome__icontains=value) |
            Q(empresa__nome__icontains=value) |
            Q(novo_preco_custo__icontains=value) |
            Q(novo_preco_venda__icontains=value)
        )
