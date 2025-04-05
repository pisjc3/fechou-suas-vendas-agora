from django.urls import path
from .views import ProdutoListView, ProdutoDetailsView, ProdutoCreateView, ProdutoUpdateView, ProdutoChangeStatus, ProdutoDeleteView

urlpatterns = [
    path('', ProdutoListView.as_view(), name='produto_list'),
    path('<int:pk>/', ProdutoDetailsView.as_view(), name='produto_details'),
    path('criar/', ProdutoCreateView.as_view(), name='produto_create'),
    path('editar/<int:pk>/', ProdutoUpdateView.as_view(), name='produto_update'),
    path('produto/<int:pk>/change-status/',
         ProdutoChangeStatus.as_view(), name='produto_change_status'),
    path("produtos/<int:pk>/deletar/",
         ProdutoDeleteView.as_view(), name="produto_delete"),
]
