import factory
from crm_apps.crm.produto.models import Produto
from crm_apps.tests.factories.categoria import CategoriaFactory
from crm_apps.tests.factories.empresa import EmpresaFactory
from crm_apps.tests.factories.user import UserFactory


class ProdutoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Produto

    nome = factory.Faker('word')
    descricao = factory.Faker('sentence')
    categoria = factory.SubFactory(CategoriaFactory)
    empresa = factory.SubFactory(EmpresaFactory)
    quantidade_estoque = factory.Faker('random_number', digits=3)
    unidade_medida = factory.Faker('random_element', elements=[
                                   e[0] for e in Produto.UnidadeMedida.choices])
    preco_custo = factory.Faker('random_number', digits=3)
    preco_venda = factory.Faker('random_number', digits=3)
    criado_por = factory.SubFactory(UserFactory)
    status = Produto.Status.ATIVO
