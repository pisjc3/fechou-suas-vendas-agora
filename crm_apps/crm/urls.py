from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('empresa/', include('crm_apps.crm.empresa.urls')),
    path('cliente/', include('crm_apps.crm.cliente.urls')),
    path('categoria/', include('crm_apps.crm.categoria.urls')),
]
