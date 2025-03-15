
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from crm_apps.crm.empresa.models import Empresa
from crm_apps.crm.usuario_empresa.models import UsuarioEmpresa


@method_decorator(login_required, name='dispatch')
class EmpresaList(ListView):
    model = Empresa
    template_name = 'empresa/list.html'
    context_object_name = 'data'


@method_decorator(login_required, name='dispatch')
class EmpresaDetails(DetailView):
    model = Empresa
    template_name = 'empresa/index.html'
    context_object_name = 'data'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not UsuarioEmpresa.objects.filter(usuario=self.request.user, empresa=obj).exists():
            return None
        return obj
