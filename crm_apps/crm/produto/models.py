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

    class UnidadeMedida(models.TextChoices):
        UNIDADE = 'un', _('Unidade')
        QUILOGRAMA = 'kg', _('Quilograma')
        LITRO = 'litro', _('Litro')
        METRO = 'm', _('Metro')
        PACOTE = 'pacote', _('Pacote')
        CAIXA = 'caixa', _('Caixa')
        OUTRO = 'outro', _('Outro')

    TIPOS_UNIDADE_PRODUTO_QUANTIDADE_MEDIDA_INTEIRA = [
        UnidadeMedida.UNIDADE,
        UnidadeMedida.CAIXA,
        UnidadeMedida.PACOTE,
    ]

    nome = models.CharField(max_length=255)
    descricao = models.TextField(max_length=255, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    quantidade_estoque = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    unidade_medida = models.CharField(
        max_length=32, choices=UnidadeMedida.choices, default=UnidadeMedida.UNIDADE)
    preco_custo = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, editable=True)
    preco_venda = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, editable=True)
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

    @classmethod
    def unidade_requer_inteiro(cls, unidade: str) -> bool:
        return unidade.lower() in {u.lower() for u in cls.TIPOS_UNIDADE_PRODUTO_QUANTIDADE_MEDIDA_INTEIRA}
