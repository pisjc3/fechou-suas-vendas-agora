from django.test import TestCase
from crm_apps.tests.factories.cliente import ClienteFactory
from crm_apps.tests.factories.empresa import EmpresaFactory
from crm_apps.tests.factories.user import UserFactory


class ClienteModelTest(TestCase):

    def test_create_cliente(self):
        empresa = EmpresaFactory.create()
        usuario = UserFactory.create()

        cliente = ClienteFactory.create(empresa=empresa, criado_por=usuario)

        self.assertEqual(cliente.nome, cliente.nome)
        self.assertEqual(cliente.empresa, empresa)
        self.assertEqual(cliente.criado_por, usuario)

    def test_cliente_str_method(self):
        cliente = ClienteFactory.create()
        self.assertEqual(str(cliente), cliente.nome)
