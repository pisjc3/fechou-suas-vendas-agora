import factory
from crm_apps.crm.cliente.models import Cliente
from crm_apps.tests.factories.empresa import EmpresaFactory
from crm_apps.tests.factories.user import UserFactory


class ClienteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cliente

    nome = factory.Faker("name")
    empresa = factory.SubFactory(EmpresaFactory)
    criado_por = factory.SubFactory(UserFactory)
