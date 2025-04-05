from django.db import models
from crm_apps.common.models import BaseModel
from crm_apps.users.models import CustomUser
from crm_apps.crm.empresa.models import Empresa


class Categoria(BaseModel):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(max_length=255, blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    criado_por = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
