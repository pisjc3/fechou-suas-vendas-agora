import factory
from crm_apps.crm.empresa.models import Empresa
from crm_apps.tests.factories.user import UserFactory


class EmpresaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Empresa

    nome = factory.Faker("company")
    criado_por = factory.SubFactory(UserFactory)
