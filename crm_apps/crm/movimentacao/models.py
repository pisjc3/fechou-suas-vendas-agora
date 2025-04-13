from django.db import models
from crm_apps.common.models import BaseModel
from crm_apps.users.models import CustomUser
from crm_apps.crm.empresa.models import Empresa
from crm_apps.crm.produto.models import Produto
from crm_apps.crm.cliente.models import Cliente


class Movimentacao(BaseModel):
    class TipoMovimentacao(models.TextChoices):
        COMPRA = 'compra', 'Compra'
        VENDA = 'venda', 'Venda'

    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name='movimentacoes')
    tipo = models.CharField(max_length=10, choices=TipoMovimentacao.choices)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         help_text="Preço unitário desta movimentação")
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True,
                                help_text="Cliente (para venda)")
    novo_preco_custo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                           help_text="Novo preço de custo (opcional, para compra)")
    novo_preco_venda = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                           help_text="Novo preço de venda (opcional, para compra)")
    criado_por = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome} - ({self.quantidade})"
