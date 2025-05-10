from django.test import TestCase
from crm_apps.crm.produto.models import Produto
from crm_apps.tests.factories.categoria import CategoriaFactory
from crm_apps.tests.factories.produto import ProdutoFactory
from crm_apps.tests.factories.empresa import EmpresaFactory
from crm_apps.tests.factories.user import UserFactory


class ProdutoModelTest(TestCase):

    def test_create_produto(self):
        categoria = CategoriaFactory.create()
        empresa = EmpresaFactory.create()
        usuario = UserFactory.create()

        produto = ProdutoFactory.create(
            categoria=categoria, empresa=empresa, criado_por=usuario, status=Produto.Status.ATIVO)

        self.assertEqual(produto.nome, produto.nome)
        self.assertEqual(produto.categoria, categoria)
        self.assertEqual(produto.empresa, empresa)
        self.assertEqual(produto.criado_por, usuario)
        self.assertTrue(produto.quantidade_estoque >= 0)
        self.assertIn(produto.status, [choice[0]
                      for choice in Produto.Status.choices])

    def test_produto_str_method(self):
        produto = ProdutoFactory.create()
        self.assertEqual(str(produto), produto.nome)

    def test_produto_unidade_medida(self):
        produto = ProdutoFactory.create()
        self.assertIn(produto.unidade_medida, [
            choice[0] for choice in Produto.UnidadeMedida.choices])
