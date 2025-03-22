from .models import Empresa
from typing import Optional
from django.contrib.auth.models import User


def criar_empresa(*,
                  nome: str,
                  cnpj: Optional[str] = None,
                  endereco: Optional[str] = None,
                  telefone: Optional[str] = None,
                  usuario: User) -> Empresa:

    empresa = Empresa(
        nome=nome,
        cnpj=cnpj,
        endereco=endereco,
        telefone=telefone,
        criado_por=usuario,
    )

    empresa.clean()
    empresa.save()
