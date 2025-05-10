from django.test import TestCase
from crm_apps.tests.factories.empresa import EmpresaFactory
from crm_apps.tests.factories.user import UserFactory


class EmpresaModelTest(TestCase):

    def test_create_empresa(self):
        usuario = UserFactory.create()
        empresa = EmpresaFactory.create(criado_por=usuario)

        self.assertEqual(empresa.nome, empresa.nome)
        self.assertEqual(empresa.criado_por, usuario)

    def test_empresa_str_method(self):
        empresa = EmpresaFactory.create()

        self.assertEqual(str(empresa), empresa.nome)
