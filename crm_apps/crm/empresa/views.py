
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from crm_apps.crm.empresa.models import Empresa
from django.views.generic import View
from crm_apps.crm.usuario_empresa.models import UsuarioEmpresa
from .forms import EmpresaCreationForm
from crm_apps.crm.util.decorators import superadmin_required
from .services import criar_empresa


@method_decorator(login_required, name='dispatch')
class EmpresaListView(ListView):
    model = Empresa
    template_name = 'empresa/empresa_list.html'
    context_object_name = 'data'


@method_decorator(login_required, name='dispatch')
class EmpresaDetailsView(DetailView):
    model = Empresa
    template_name = 'empresa/empresa_detail.html'
    context_object_name = 'data'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not UsuarioEmpresa.objects.filter(usuario=self.request.user, empresa=obj).exists():
            return None
        return obj


@method_decorator(login_required, name='dispatch')
@method_decorator(superadmin_required, name='dispatch')
class EmpresaCreateView(View):
    form_class = EmpresaCreationForm
    template_name = 'empresa/empresa_create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            nome = form.cleaned_data['nome']
            cnpj = form.cleaned_data['cnpj']
            endereco = form.cleaned_data['endereco']
            telefone = form.cleaned_data['telefone']
            usuario = request.user

            criar_empresa(nome=nome, cnpj=cnpj, endereco=endereco,
                          telefone=telefone, usuario=usuario)
            return redirect('/')

        return render(request, self.template_name, {'form': form})
