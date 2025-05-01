from django.urls import path
from .views import VendaCreateView, CompraCreateView, MovimentacaoListView, VendaListView, CompraListView

urlpatterns = [
    path('', MovimentacaoListView.as_view(), name='movimentacao_list'),
    path('venda/', VendaListView.as_view(), name='venda_list'),
    path('entrada/', CompraListView.as_view(), name='compra_list'),
    path('nova-venda/', VendaCreateView.as_view(), name='venda_create'),
    path('nova-entrada/', CompraCreateView.as_view(), name='compra_create'),
]
