from django.db import models
from crm_apps.common.models import BaseModel
from crm_apps.users.models import CustomUser
from crm_apps.crm.empresa.models import Empresa


class Cliente(BaseModel):
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=500, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    data_nascimento = models.DateField(blank=True, null=True)
    criado_por = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
