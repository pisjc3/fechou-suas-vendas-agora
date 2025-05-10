import pytest
from decimal import Decimal
from crm_apps.tests.factories.movimentacao import MovimentacaoFactory
from crm_apps.crm.movimentacao.models import Movimentacao


@pytest.mark.django_db
class TestMovimentacaoModel:

    def test_criacao_movimentacao_compra(self):
        movimentacao = MovimentacaoFactory(
            tipo=Movimentacao.TipoMovimentacao.COMPRA, cliente=None)

        assert movimentacao.pk is not None
        assert movimentacao.tipo == Movimentacao.TipoMovimentacao.COMPRA
        assert movimentacao.cliente is None
        assert isinstance(movimentacao.quantidade, Decimal)
        assert isinstance(movimentacao.preco_unitario, Decimal)
        assert str(
            movimentacao) == f"Compra - {movimentacao.produto.nome} - ({movimentacao.quantidade})"

    def test_criacao_movimentacao_venda(self):
        movimentacao = MovimentacaoFactory(
            tipo=Movimentacao.TipoMovimentacao.VENDA)

        assert movimentacao.pk is not None
        assert movimentacao.tipo == Movimentacao.TipoMovimentacao.VENDA
        assert movimentacao.cliente is not None
        assert str(
            movimentacao) == f"Venda - {movimentacao.produto.nome} - ({movimentacao.quantidade})"
