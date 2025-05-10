from .models import Empresa
from typing import Optional
from crm_apps.users.models import CustomUser


def criar_empresa(*,
                  nome: str,
                  cnpj: Optional[str] = None,
                  endereco: Optional[str] = None,
                  telefone: Optional[str] = None,
                  criado_por: CustomUser) -> Empresa:

    empresa = Empresa(
        nome=nome,
        cnpj=cnpj,
        endereco=endereco,
        telefone=telefone,
        criado_por=criado_por,
    )

    empresa.clean()
    empresa.save()

    return empresa
