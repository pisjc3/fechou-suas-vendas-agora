import factory
from crm_apps.crm.categoria.models import Categoria
from crm_apps.tests.factories.empresa import EmpresaFactory
from crm_apps.tests.factories.user import UserFactory


class CategoriaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Categoria

    nome = factory.Faker("word")
    descricao = factory.Faker("sentence")
    empresa = factory.SubFactory(EmpresaFactory)
    criado_por = factory.SubFactory(UserFactory)
