from django.urls import path
from .views import ClienteListView, ClienteDetailsView, ClienteCreateView

urlpatterns = [
    path('', ClienteListView.as_view(), name='cliente_list'),
    path('<int:pk>/', ClienteDetailsView.as_view(), name='cliente_detail'),
    path('criar/', ClienteCreateView.as_view(), name='cliente_create'),
]
