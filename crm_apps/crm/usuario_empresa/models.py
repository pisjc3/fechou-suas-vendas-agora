from django.db import models
from django.contrib.auth.models import User
from crm_apps.crm.empresa.models import Empresa


class UsuarioEmpresa(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='empresas')
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name='usuarios')

    class Meta:
        unique_together = ('usuario', 'empresa')

    def __str__(self):
        return f"{self.usuario.username} - {self.empresa.nome}"
