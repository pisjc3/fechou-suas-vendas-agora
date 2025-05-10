from django.test import TestCase
from crm_apps.tests.factories.categoria import CategoriaFactory
from crm_apps.tests.factories.empresa import EmpresaFactory
from crm_apps.tests.factories.user import UserFactory


class CategoriaModelTest(TestCase):
    def test_create_categoria(self):
        empresa = EmpresaFactory.create()
        usuario = UserFactory.create()

        categoria = CategoriaFactory.create(
            empresa=empresa, criado_por=usuario)

        self.assertEqual(categoria.empresa, empresa)
        self.assertEqual(categoria.criado_por, usuario)
        self.assertIsInstance(categoria.nome, str)

    def test_categoria_str_method(self):
        categoria = CategoriaFactory.create()
        self.assertEqual(str(categoria), categoria.nome)
