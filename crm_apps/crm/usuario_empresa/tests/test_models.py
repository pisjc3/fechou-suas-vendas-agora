# crm_apps/crm/usuario_empresa/tests/test_models.py

from django.test import TestCase
from crm_apps.tests.factories.user import UserFactory
from crm_apps.tests.factories.empresa import EmpresaFactory
from crm_apps.tests.factories.usuario_empresa import UsuarioEmpresaFactory


class UsuarioEmpresaModelTest(TestCase):

    def test_create_usuario_empresa(self):
        usuario = UserFactory.create()
        empresa = EmpresaFactory.create()

        usuario_empresa = UsuarioEmpresaFactory.create(
            usuario=usuario, empresa=empresa)

        self.assertEqual(usuario_empresa.usuario, usuario)
        self.assertEqual(usuario_empresa.empresa, empresa)

    def test_usuario_empresa_str_method(self):
        usuario_empresa = UsuarioEmpresaFactory.create()
        expected_str = f"{usuario_empresa.usuario} - {usuario_empresa.empresa}"
        self.assertEqual(str(usuario_empresa), expected_str)
