from crm_apps.users.models import CustomUser
from crm_apps.common.models import BaseModel
from django.db import models
from django.core.exceptions import ValidationError
from crm_apps.common.util.validators import telefone_validator, cnpj_validator


class Empresa(BaseModel):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    endereco = models.CharField(max_length=500, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    criado_por = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    def clean(self):
        if self.cnpj:
            if not cnpj_validator(self.cnpj):
                raise ValidationError('CNPJ inválido.')

        if self.cnpj and Empresa.objects.filter(cnpj=self.cnpj).exclude(id=self.id).exists():
            raise ValidationError('Já existe uma empresa com este CNPJ.')

        if self.telefone:
            telefone_validator(self.telefone)

        super().clean()
