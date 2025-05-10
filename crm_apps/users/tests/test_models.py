import pytest
from crm_apps.users.models import CustomUser
from crm_apps.tests.factories.user import UserFactory

pytestmark = pytest.mark.django_db


def test_user_factory_cria_usuario_valido():
    user = UserFactory()
    assert isinstance(user, CustomUser)
    assert user.email is not None
    assert user.username is not None


def test_user_str_retorna_username():
    user = UserFactory(username="usuario_teste")
    assert str(user) == "usuario_teste"
