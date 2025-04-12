from .models import Produto
from typing import Optional
from crm_apps.users.models import CustomUser
from crm_apps.crm.empresa.models import Empresa
from crm_apps.crm.categoria.models import Categoria


def create_produto(*,
                   nome: str,
                   descricao: Optional[str] = None,
                   categoria: Categoria,
                   empresa: Empresa,
                   quantidade_inicial: Optional[float] = 0,
                   preco_custo: Optional[float] = 0,
                   preco_venda: Optional[float] = 0,
                   unidade_medida: str,
                   criado_por: CustomUser) -> Produto:

    produto = Produto(
        nome=nome,
        descricao=descricao,
        categoria=categoria,
        empresa=empresa,
        quantidade_estoque=quantidade_inicial or 0,
        preco_custo=preco_custo or 0,
        preco_venda=preco_venda or 0,
        unidade_medida=unidade_medida,
        criado_por=criado_por,
    )

    produto.clean()
    produto.save()


def update_produto(*,
                   produto_id: int,
                   nome: str,
                   descricao: Optional[str] = None,
                   categoria: Categoria,
                   preco_custo: float,
                   preco_venda: float,
                   status: Optional[str] = None,
                   ) -> Produto:

    produto = Produto.objects.get(id=produto_id)

    if nome:
        produto.nome = nome
    if descricao:
        produto.descricao = descricao
    if categoria:
        produto.categoria = categoria
    if preco_custo:
        produto.preco_custo = preco_custo
    if preco_venda:
        produto.preco_venda = preco_venda
    if status is not None:
        produto.status = status

    produto.clean()
    produto.save()

    return produto
