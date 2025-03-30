from typing import Optional
from crm_apps.crm.usuario_empresa.models import UsuarioEmpresa
from crm_apps.crm.empresa.models import Empresa


def get_usuario_empresa(*, usuario_id: int, empresa_id: int) -> Optional[UsuarioEmpresa]:
    return UsuarioEmpresa.objects.filter(usuario_id=usuario_id, empresa_id=empresa_id).first()


def get_empresa_do_usuario(*, usuario_id: int) -> Optional[Empresa]:
    usuario_empresa = UsuarioEmpresa.objects.filter(
        usuario_id=usuario_id).first()
    return usuario_empresa.empresa if usuario_empresa else None
