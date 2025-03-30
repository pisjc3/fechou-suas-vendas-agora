from .models import Cliente
from datetime import date
from typing import Optional
from crm_apps.users.models import CustomUser
from crm_apps.crm.empresa.models import Empresa


def criar_cliente(*,
                  nome: str,
                  data_nascimento: Optional[date] = None,
                  endereco: Optional[str] = None,
                  telefone: Optional[str] = None,
                  empresa: Empresa,
                  criado_por: CustomUser) -> Cliente:

    cliente = Cliente(
        nome=nome,
        data_nascimento=data_nascimento,
        endereco=endereco,
        telefone=telefone,
        empresa=empresa,
        criado_por=criado_por,
    )

    cliente.clean()
    cliente.save()


def update_cliente(*,
                   cliente_id: int,
                   nome: Optional[str] = None,
                   data_nascimento: Optional[date] = None,
                   endereco: Optional[str] = None,
                   telefone: Optional[str] = None,
                   ) -> Cliente:

    cliente = Cliente.objects.get(id=cliente_id)

    if nome:
        cliente.nome = nome
    if data_nascimento:
        cliente.data_nascimento = data_nascimento
    if endereco:
        cliente.endereco = endereco
    if telefone:
        cliente.telefone = telefone

    cliente.clean()
    cliente.save()

    return cliente
