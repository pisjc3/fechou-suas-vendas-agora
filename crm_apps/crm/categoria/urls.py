from django.urls import path
from .views import CategoriaListView, CategoriaDetailsView, CategoriaCreateView, CategoriaUpdateView

urlpatterns = [
    path('', CategoriaListView.as_view(), name='categoria_list'),
    path('<int:pk>/', CategoriaDetailsView.as_view(), name='categoria_details'),
    path('criar/', CategoriaCreateView.as_view(), name='categoria_create'),
    path('editar/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria_update'),
]
