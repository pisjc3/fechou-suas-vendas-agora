from crm_apps.crm.usuario_empresa.models import UsuarioEmpresa


def usuario_pertence_empresa(*, usuario: int, empresa: int) -> bool:
    """
    Verifica se o usuário é da empresa, ou seja,
    se há um relacionamento no modelo UsuarioEmpresa.
    """
    return UsuarioEmpresa.objects.filter(usuario=usuario, empresa=empresa).exists()
