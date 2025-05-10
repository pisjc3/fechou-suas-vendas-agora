# crm_apps/tests/factories/movimentacao.py

import factory
from crm_apps.crm.movimentacao.models import Movimentacao
from crm_apps.tests.factories.produto import ProdutoFactory
from crm_apps.tests.factories.empresa import EmpresaFactory
from crm_apps.tests.factories.user import UserFactory
from crm_apps.tests.factories.cliente import ClienteFactory


class MovimentacaoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movimentacao

    produto = factory.SubFactory(ProdutoFactory)
    tipo = factory.Iterator(
        [Movimentacao.TipoMovimentacao.COMPRA, Movimentacao.TipoMovimentacao.VENDA])
    quantidade = factory.Faker(
        "pydecimal", left_digits=2, right_digits=2, positive=True)
    preco_unitario = factory.Faker(
        "pydecimal", left_digits=2, right_digits=2, positive=True)
    cliente = factory.SubFactory(ClienteFactory)
    novo_preco_custo = factory.Faker(
        "pydecimal", left_digits=2, right_digits=2, positive=True)
    novo_preco_venda = factory.Faker(
        "pydecimal", left_digits=2, right_digits=2, positive=True)
    criado_por = factory.SubFactory(UserFactory)
    empresa = factory.SubFactory(EmpresaFactory)
