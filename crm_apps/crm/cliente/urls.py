from django.urls import path
from .views import ClienteListView, ClienteDetailsView, ClienteCreateView, ClienteUpdateView

urlpatterns = [
    path('', ClienteListView.as_view(), name='cliente_list'),
    path('<int:pk>/', ClienteDetailsView.as_view(), name='cliente_details'),
    path('criar/', ClienteCreateView.as_view(), name='cliente_create'),
    path('editar/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_update'),
]
