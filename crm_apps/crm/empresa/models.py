from django.contrib.auth.models import User
from crm_apps.common.models import BaseModel
from django.db import models


class Empresa(BaseModel):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True, blank=True, null=True)
    endereco = models.CharField(max_length=500, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    criado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome
