from .models import Categoria
from typing import Optional
from crm_apps.users.models import CustomUser
from crm_apps.crm.empresa.models import Empresa


def create_categoria(*,
                     nome: str,
                     descricao: Optional[str] = None,
                     empresa: Empresa,
                     criado_por: CustomUser) -> Categoria:

    categoria = Categoria(
        nome=nome,
        descricao=descricao,
        empresa=empresa,
        criado_por=criado_por,
    )

    categoria.clean()
    categoria.save()


def update_categoria(*,
                     categoria_id: int,
                     nome: str,
                     descricao: Optional[str] = None
                     ) -> Categoria:

    categoria = Categoria.objects.get(id=categoria_id)

    if nome:
        categoria.nome = nome
    if descricao:
        categoria.descricao = descricao

    categoria.clean()
    categoria.save()

    return categoria
