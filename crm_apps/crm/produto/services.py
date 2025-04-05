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
                   criado_por: CustomUser) -> Produto:

    produto = Produto(
        nome=nome,
        descricao=descricao,
        categoria=categoria,
        empresa=empresa,
        criado_por=criado_por,
    )

    produto.clean()
    produto.save()


def update_produto(*,
                   produto_id: int,
                   nome: str,
                   descricao: Optional[str] = None,
                   categoria: Categoria,
                   status: Optional[str] = None,
                   ) -> Produto:

    produto = Produto.objects.get(id=produto_id)

    if nome:
        produto.nome = nome
    if descricao:
        produto.descricao = descricao
    if categoria:
        produto.categoria = categoria
    if status is not None:
        produto.status = status

    produto.clean()
    produto.save()

    return produto
