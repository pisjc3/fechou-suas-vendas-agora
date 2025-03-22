from crm_apps.crm.util.validators import telefone_validator
from django.core.exceptions import ValidationError
from .models import Empresa
from crm_apps.crm.util.validators import telefone_validator, cnpj_validator
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
