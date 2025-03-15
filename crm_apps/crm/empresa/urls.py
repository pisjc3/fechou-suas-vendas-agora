from django.urls import path
from .views import EmpresaList, EmpresaDetails

urlpatterns = [
    path('', EmpresaList.as_view(), name='EmpresaList'),
    path('<int:pk>/', EmpresaDetails.as_view(), name='EmpresaDetails'),
]
