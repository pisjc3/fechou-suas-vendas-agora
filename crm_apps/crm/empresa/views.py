from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from crm_apps.crm.empresa.models import Empresa
from django.views.generic import View
from .forms import EmpresaCreationForm
from crm_apps.crm.util.decorators import superadmin_required
from .services import criar_empresa
from django.contrib import messages
from django.http import Http404
from crm_apps.crm.util.selectors import get_usuario_empresa


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

        # verifica se o usuário é superadmin ou tem permissão para visualizar a empresa
        if self.request.user.is_superuser:
            return obj

        usuario_empresa = get_usuario_empresa(
            usuario_id=self.request.user.id, empresa_id=obj.id)

        # para outros usuários, verifica se existe uma associação no modelo UsuarioEmpresa
        if not usuario_empresa:
            raise Http404(
                "Você não tem permissão para visualizar esta empresa.")

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

            try:
                criar_empresa(nome=nome, cnpj=cnpj, endereco=endereco,
                              telefone=telefone, criado_por=usuario)
                messages.success(request, "Empresa criada com sucesso!")
                return redirect('/')
            except Exception as e:
                messages.error(request, "Erro ao criar a empresa")

        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")

        return render(request, self.template_name, {'form': form})
