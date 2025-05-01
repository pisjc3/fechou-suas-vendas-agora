from decimal import Decimal
from typing import Optional
from django.db import transaction
from crm_apps.crm.movimentacao.models import Movimentacao
from crm_apps.crm.produto.models import Produto
from crm_apps.crm.cliente.models import Cliente
from crm_apps.crm.empresa.models import Empresa


@transaction.atomic
def create_venda(*,
                 produto: Produto,
                 quantidade: Decimal,
                 preco_unitario: Optional[Decimal] = None,
                 cliente: Optional[Cliente] = None,
                 empresa: Empresa,
                 criado_por) -> Movimentacao:

    preco_unitario = preco_unitario or produto.preco_venda
    quantidade_estoque = produto.quantidade_estoque

    if quantidade > 0 and quantidade > quantidade_estoque:
        quantidade_str = str(quantidade)
        if Produto.unidade_requer_inteiro(produto.unidade_medida):
            estoque_str = str(int(quantidade_estoque)).replace('.', ',')
        else:
            estoque_str = str(quantidade_estoque).replace('.', ',')

        raise ValueError(
            f"Quantidade solicitada ({quantidade_str}) excede o estoque disponível de ({estoque_str})."
        )
    produto.quantidade_estoque -= Decimal(quantidade)

    produto.save()

    movimentacao = Movimentacao.objects.create(
        produto=produto,
        tipo=Movimentacao.TipoMovimentacao.VENDA,
        quantidade=quantidade,
        preco_unitario=preco_unitario,
        cliente=cliente,
        empresa=empresa,
        criado_por=criado_por
    )

    return movimentacao


@transaction.atomic
def create_compra(*,
                  produto: Produto,
                  quantidade: Decimal,
                  novo_preco_custo: Optional[Decimal] = None,
                  novo_preco_venda: Optional[Decimal] = None,
                  cliente: Optional[Cliente] = None,
                  empresa: Empresa,
                  criado_por) -> Movimentacao:

    produto.quantidade_estoque += Decimal(quantidade)

    if novo_preco_custo is not None:
        produto.preco_custo = novo_preco_custo
    if novo_preco_venda is not None:
        produto.preco_venda = novo_preco_venda

    produto.save()

    movimentacao = Movimentacao.objects.create(
        produto=produto,
        tipo=Movimentacao.TipoMovimentacao.COMPRA,
        quantidade=quantidade,
        novo_preco_custo=novo_preco_custo,
        novo_preco_venda=novo_preco_venda,
        cliente=cliente,
        empresa=empresa,
        criado_por=criado_por
    )

    return movimentacao
