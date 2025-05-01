from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import VendaForm, CompraForm, VendaAdminForm, CompraAdminForm
from .models import Movimentacao
from .filters import MovimentacaoFilter
from crm_apps.common.ordering import sort_queryset
from .services import create_venda, create_compra
from crm_apps.crm.util.selectors import get_empresa_do_usuario


@method_decorator(login_required, name='dispatch')
class MovimentacaoListView(ListView):
    model = Movimentacao
    template_name = 'movimentacao/movimentacao_list.html'
    context_object_name = 'data'
    paginate_by = 10

    def get_queryset(self):
        usuario = self.request.user

        if usuario.is_superuser:
            queryset = Movimentacao.objects.all()
        else:
            empresa = get_empresa_do_usuario(usuario_id=usuario.id)
            queryset = Movimentacao.objects.filter(empresa=empresa)

        self.filterset = MovimentacaoFilter(
            self.request.GET, queryset=queryset)
        queryset_filtrado = self.filterset.qs

        sort_param = self.request.GET.get('sort', 'produto__nome')
        order_param = self.request.GET.get('order', 'asc')

        if sort_param == 'data-operacao':
            sort_param = 'data_criacao'
        if sort_param == 'preco-un':
            sort_param = 'preco_unitario'
        if sort_param == 'novo-preco-custo':
            sort_param = 'novo_preco_custo'
        if sort_param == 'novo-preco-venda':
            sort_param = 'novo_preco_venda'

        queryset_ordenado = sort_queryset(
            queryset_filtrado, sort_param, order_param)

        return queryset_ordenado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        headers = ['Produto', 'Tipo', 'Quantidade', 'Preço un.',
                   'Novo preço custo', 'Novo preço venda', 'Cliente', 'Data operação']

        if self.request.user.is_superuser:
            headers.append("Empresa")

        context["headers"] = headers
        context["text_center_columns"] = [
            'Tipo', 'Quantidade', 'Preço un.',  'Novo preço custo', 'Novo preço venda', 'Data operação']
        return context


@method_decorator(login_required, name='dispatch')
class VendaListView(MovimentacaoListView):
    template_name = 'movimentacao/venda_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(tipo='venda')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        headers = context["headers"]
        if "Tipo" in headers:
            headers.remove("Tipo")
        if "Novo preço custo" in headers:
            headers.remove("Novo preço custo")
        if "Novo preço venda" in headers:
            headers.remove("Novo preço venda")
        context["headers"] = headers

        text_center_columns = context["text_center_columns"]
        if "Tipo" in text_center_columns:
            text_center_columns.remove("Tipo")
        context["text_center_columns"] = text_center_columns

        return context


@method_decorator(login_required, name='dispatch')
class CompraListView(MovimentacaoListView):
    template_name = 'movimentacao/compra_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(tipo='compra')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        headers = context["headers"]
        if "Tipo" in headers:
            headers.remove("Tipo")
        if "Cliente" in headers:
            headers.remove("Cliente")
        if "Preço un." in headers:
            headers.remove("Preço un.")
        context["headers"] = headers

        text_center_columns = context["text_center_columns"]
        if "Tipo" in text_center_columns:
            text_center_columns.remove("Tipo")
        context["text_center_columns"] = text_center_columns

        return context


@method_decorator(login_required, name='dispatch')
class VendaCreateView(CreateView):
    model = Movimentacao
    success_url = reverse_lazy('venda_list')
    form_class = VendaForm
    template_name = 'movimentacao/venda_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_form_class(self):
        return VendaAdminForm if self.request.user.is_superuser else VendaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo'] = Movimentacao.TipoMovimentacao.VENDA
        return context

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

        try:
            create_venda(
                produto=form.cleaned_data['produto'],
                quantidade=form.cleaned_data['quantidade'],
                preco_unitario=form.cleaned_data.get('preco_unitario'),
                cliente=form.cleaned_data.get('cliente'),
                empresa=empresa,
                criado_por=usuario,
            )
            messages.success(self.request, "Venda registrada com sucesso!")
            return redirect(self.success_url)
        except Exception as e:
            messages.error(self.request, f"Ocorreu um erro: {str(e)}")
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Por favor, corrija os erros abaixo.")
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class CompraCreateView(CreateView):
    model = CompraForm
    success_url = reverse_lazy('compra_list')
    template_name = 'movimentacao/compra_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_form_class(self):
        return CompraAdminForm if self.request.user.is_superuser else CompraForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo'] = Movimentacao.TipoMovimentacao.COMPRA
        return context

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

        try:
            create_compra(
                produto=form.cleaned_data['produto'],
                quantidade=form.cleaned_data['quantidade'],
                novo_preco_custo=form.cleaned_data.get('novo_preco_custo'),
                novo_preco_venda=form.cleaned_data.get('novo_preco_venda'),
                empresa=empresa,
                criado_por=usuario,
            )
            messages.success(self.request, "Compra registrada com sucesso!")
            return redirect(self.success_url)
        except Exception as e:
            messages.error(self.request, f"Ocorreu um erro: {str(e)}")
            return super().form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Por favor, corrija os erros abaixo.")
        return super().form_invalid(form)
