from django.db import models
from crm_apps.common.models import BaseModel
from crm_apps.users.models import CustomUser
from crm_apps.crm.empresa.models import Empresa
from crm_apps.crm.categoria.models import Categoria
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Produto(BaseModel):
    class Status(models.TextChoices):
        ATIVO = 'ativo', _('Ativo')
        INATIVO = 'inativo', _('Inativo')

    nome = models.CharField(max_length=255)
    descricao = models.TextField(max_length=255, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    criado_por = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ATIVO
    )

    def __str__(self):
        return self.nome

    def get_delete_url(self):
        return reverse('produto_delete', args=[self.id])
