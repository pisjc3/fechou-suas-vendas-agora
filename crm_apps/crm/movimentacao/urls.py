from django.urls import path
from .views import VendaCreateView, CompraCreateView

urlpatterns = [
    path('nova-venda/', VendaCreateView.as_view(), name='venda_form'),
    path('nova-compra/', CompraCreateView.as_view(), name='compra_form'),
]
