import factory
from crm_apps.tests.factories.user import UserFactory
from crm_apps.tests.factories.empresa import EmpresaFactory
from crm_apps.crm.usuario_empresa.models import UsuarioEmpresa


class UsuarioEmpresaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UsuarioEmpresa

    usuario = factory.SubFactory(UserFactory)
    empresa = factory.SubFactory(EmpresaFactory)
