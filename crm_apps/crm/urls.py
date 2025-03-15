from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('empresa/', include('crm_apps.crm.empresa.urls')),
]
