from django.urls import path
from .views import ClienteListView, ClienteDetailsView, ClienteCreateView, ClienteUpdateView, ClientesPorEmpresaView

urlpatterns = [
    path('', ClienteListView.as_view(), name='cliente_list'),
    path('<int:pk>/', ClienteDetailsView.as_view(), name='cliente_details'),
    path('criar/', ClienteCreateView.as_view(), name='cliente_create'),
    path('editar/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('api/clientes-por-empresa/', ClientesPorEmpresaView.as_view(),
         name='clientes-por-empresa'),
]
