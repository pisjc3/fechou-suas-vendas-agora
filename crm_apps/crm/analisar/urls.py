from django.urls import path
from .views import AnalisarListView

urlpatterns = [
    path('', AnalisarListView.as_view(), name='analisar_list'),
]
