from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Categoria
from .filters import CategoriaFilter
from .forms import CategoriaCreationAdminForm, CategoriaCreationFormBase, CategoriaUpdateForm
from .services import create_categoria, update_categoria
from crm_apps.crm.util.selectors import get_usuario_empresa, get_empresa_do_usuario
from django.urls import reverse_lazy
from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages
from crm_apps.common.ordering import sort_queryset
from crm_apps.common.util.formats import format_date


@method_decorator(login_required, name='dispatch')
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria/categoria_list.html'
    context_object_name = 'data'
    paginate_by = 10

    def get_queryset(self):
        usuario = self.request.user

        if usuario.is_superuser:
            queryset = Categoria.objects.all()
        else:
            empresa = get_empresa_do_usuario(usuario_id=usuario.id)
            queryset = Categoria.objects.filter(empresa=empresa)

        self.filterset = CategoriaFilter(self.request.GET, queryset=queryset)
        queryset_filtrado = self.filterset.qs

        sort_param = self.request.GET.get('sort', 'nome')
        order_param = self.request.GET.get('order', 'asc')

        if sort_param == 'data-de-criacao':
            sort_param = 'data_criacao'
        if sort_param == 'data-de-edicao':
            sort_param = 'data_edicao'

        queryset_ordenado = sort_queryset(
            queryset_filtrado, sort_param, order_param)

        return queryset_ordenado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        headers = ["Nome", "Descrição", "Data de criação", "Data de edição"]

        if self.request.user.is_superuser:
            headers.append("Empresa")

        context["headers"] = headers
        return context


@method_decorator(login_required, name='dispatch')
class CategoriaDetailsView(DetailView):
    model = Categoria
    template_name = 'categoria/categoria_details.html'
    context_object_name = 'data'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        usuario = self.request.user

        if usuario.is_superuser:
            return obj

        usuario_empresa = get_usuario_empresa(
            usuario_id=usuario.id, empresa_id=obj.empresa.id)

        if not usuario_empresa:
            raise Http404(
                "Você não tem permissão para visualizar esta categoria.")

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria = context['data']

        context['details'] = {
            'Nome': categoria.nome,
            'Descrição': categoria.descricao,
            'Data de criação': format_date(categoria.data_criacao),
            'Data de edição': format_date(categoria.data_edicao),
        }
        context['update_url'] = f"/categoria/editar/{categoria.id}/"

        return context


@method_decorator(login_required, name='dispatch')
class CategoriaCreateView(CreateView):
    template_name = 'categoria/categoria_create.html'
    success_url = reverse_lazy('categoria_list')

    def get_form_class(self):
        return CategoriaCreationAdminForm if self.request.user.is_superuser else CategoriaCreationFormBase

    def form_valid(self, form):
        usuario = self.request.user
        empresa = None

        if usuario.is_superuser:
            empresa = form.cleaned_data['empresa']
        else:
            empresa = get_empresa_do_usuario(usuario_id=usuario.id)
            if not empresa:
                messages.error(
                    self.request, "Você não tem uma empresa associada.")
                return super().form_invalid(form)

        create_categoria(
            nome=form.cleaned_data['nome'],
            descricao=form.cleaned_data.get('descricao'),
            empresa=empresa,
            criado_por=usuario
        )

        messages.success(self.request, "Categoria criada com sucesso!")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(
            self.request, "Por favor, corrija os erros abaixo.")
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class CategoriaUpdateView(UpdateView):
    model = Categoria
    template_name = 'categoria/categoria_update.html'
    context_object_name = 'categoria'
    form_class = CategoriaUpdateForm

    def get_object(self, queryset=None):
        usuario = self.request.user
        categoria = super().get_object(queryset)

        if usuario.is_superuser:
            return categoria

        usuario_empresa = get_usuario_empresa(
            usuario_id=usuario.id, empresa_id=categoria.empresa.id)

        if not usuario_empresa:
            raise Http404("Você não tem permissão para editar esta categoria.")

        return categoria

    def form_valid(self, form):
        categoria = self.get_object()

        update_categoria(
            categoria_id=categoria.id,
            nome=form.cleaned_data['nome'],
            descricao=form.cleaned_data.get('descricao'),
        )

        messages.success(self.request, "Categoria atualizada com sucesso!")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Por favor, corrija os erros abaixo.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('categoria_details', kwargs={'pk': self.object.pk})
