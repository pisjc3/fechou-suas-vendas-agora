from django.urls import path
from .views import EmpresaListView, EmpresaDetailsView, EmpresaCreateView

urlpatterns = [
    path('', EmpresaListView.as_view(), name='empresa_list'),
    path('<int:pk>/', EmpresaDetailsView.as_view(), name='empresa_details'),
    path('criar/', EmpresaCreateView.as_view(), name='empresa_create'),
]
