from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from crm_apps.crm.cliente.models import Cliente
from crm_apps.crm.util.selectors import get_usuario_empresa, get_empresa_do_usuario
from .forms import ClienteCreationFormBase, ClienteCreationAdminForm, ClienteUpdateForm
from .services import criar_cliente, update_cliente
from .filters import ClienteFilter
from django.urls import reverse_lazy
from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages
from crm_apps.common.ordering import sort_queryset
from crm_apps.common.util.formats import format_date
from django.utils.dateformat import DateFormat


@method_decorator(login_required, name='dispatch')
class ClienteListView(ListView):
    model = Cliente
    template_name = 'cliente/cliente_list.html'
    context_object_name = 'data'
    paginate_by = 10

    def get_queryset(self):
        usuario = self.request.user

        if usuario.is_superuser:
            queryset = Cliente.objects.all()
        else:
            empresa = get_empresa_do_usuario(usuario_id=usuario.id)
            queryset = Cliente.objects.filter(empresa=empresa)

        self.filterset = ClienteFilter(self.request.GET, queryset=queryset)
        queryset_filtrado = self.filterset.qs

        sort_param = self.request.GET.get('sort')
        order_param = self.request.GET.get('order')

        if sort_param == 'data-de-nascimento':
            sort_param = 'data_nascimento'
        if sort_param == 'data-de-criacao':
            sort_param = 'data_criacao'

        queryset_ordenado = sort_queryset(
            queryset_filtrado, sort_param, order_param)

        return queryset_ordenado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        headers = ["Nome", "Data de nascimento",
                   "Endereço", "Telefone", "Data de criação"]

        if self.request.user.is_superuser:
            headers.append("Empresa")

        context["headers"] = headers
        return context


@method_decorator(login_required, name='dispatch')
class ClienteDetailsView(DetailView):
    model = Cliente
    template_name = 'cliente/cliente_details.html'
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
                "Você não tem permissão para visualizar este cliente.")

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = context['data']

        context['details'] = {
            'Nome': cliente.nome,
            'Endereço': cliente.endereco,
            'Telefone': cliente.telefone,
            'Data de nascimento': format_date(cliente.data_nascimento),
        }
        context['update_url'] = f"/cliente/editar/{cliente.id}/"

        return context


@method_decorator(login_required, name='dispatch')
class ClienteCreateView(CreateView):
    template_name = 'cliente/cliente_create.html'
    success_url = reverse_lazy('cliente_list')

    def get_form_class(self):
        return ClienteCreationAdminForm if self.request.user.is_superuser else ClienteCreationFormBase

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

        criar_cliente(
            nome=form.cleaned_data['nome'],
            data_nascimento=form.cleaned_data.get('data_nascimento'),
            endereco=form.cleaned_data.get('endereco'),
            telefone=form.cleaned_data.get('telefone'),
            empresa=empresa,
            criado_por=usuario
        )

        messages.success(self.request, "Cliente criado com sucesso!")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(
            self.request, "Por favor, corrija os erros abaixo.")
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class ClienteUpdateView(UpdateView):
    model = Cliente
    template_name = 'cliente/cliente_update.html'
    context_object_name = 'cliente'
    form_class = ClienteUpdateForm

    def get_object(self, queryset=None):
        usuario = self.request.user
        cliente = super().get_object(queryset)

        if cliente.data_nascimento:
            cliente.data_nascimento = DateFormat(
                cliente.data_nascimento).format('Y-m-d')

        if usuario.is_superuser:
            return cliente

        usuario_empresa = get_usuario_empresa(
            usuario_id=usuario.id, empresa_id=cliente.empresa.id)

        if not usuario_empresa:
            raise Http404("Você não tem permissão para editar este cliente.")

        return cliente

    def form_valid(self, form):
        cliente = self.get_object()

        update_cliente(
            cliente_id=cliente.id,
            nome=form.cleaned_data['nome'],
            data_nascimento=form.cleaned_data.get('data_nascimento'),
            endereco=form.cleaned_data.get('endereco'),
            telefone=form.cleaned_data.get('telefone'),
        )

        messages.success(self.request, "Cliente atualizado com sucesso!")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Por favor, corrija os erros abaixo.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('cliente_details', kwargs={'pk': self.object.pk})
