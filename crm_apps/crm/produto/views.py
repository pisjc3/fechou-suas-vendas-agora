from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from .models import Produto
from .filters import ProdutoFilter
from .forms import ProdutoCreationAdminForm, ProdutoCreationFormBase, ProdutoUpdateForm
from .services import create_produto, update_produto
from crm_apps.crm.util.selectors import get_usuario_empresa, get_empresa_do_usuario
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib import messages
from crm_apps.common.ordering import sort_queryset
from crm_apps.common.util.formats import format_date, format_currency


@method_decorator(login_required, name='dispatch')
class ProdutoListView(ListView):
    model = Produto
    template_name = 'produto/produto_list.html'
    context_object_name = 'data'
    paginate_by = 10

    def get_queryset(self):
        usuario = self.request.user

        if usuario.is_superuser:
            queryset = Produto.objects.all()
        else:
            empresa = get_empresa_do_usuario(usuario_id=usuario.id)
            queryset = Produto.objects.filter(empresa=empresa)

        self.filterset = ProdutoFilter(self.request.GET, queryset=queryset)
        queryset_filtrado = self.filterset.qs

        sort_param = self.request.GET.get('sort', 'nome')
        order_param = self.request.GET.get('order', 'asc')

        if sort_param == 'data-de-criacao':
            sort_param = 'data_criacao'
        if sort_param == 'data-de-edicao':
            sort_param = 'data_edicao'
        if sort_param == 'qtd-em-estoque':
            sort_param = 'quantidade_estoque'
        if sort_param == 'unidade':
            sort_param = 'unidade_medida'
        if sort_param == 'preco-custo':
            sort_param = 'preco_custo'
        if sort_param == 'preco-venda':
            sort_param = 'preco_venda'

        queryset_ordenado = sort_queryset(
            queryset_filtrado, sort_param, order_param)

        return queryset_ordenado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        headers = ["Nome", "Categoria", "Qtd. em estoque", "Unidade", "Preço custo", "Preço venda",
                   "Data de criação", "Status"]

        if self.request.user.is_superuser:
            headers.append("Empresa")

        context["headers"] = headers
        context["text_center_columns"] = [
            'Qtd. em estoque', 'Unidade', 'Preço custo', 'Preço venda', 'Data de criação']
        return context


@method_decorator(login_required, name='dispatch')
class ProdutoDetailsView(DetailView):
    model = Produto
    template_name = 'produto/produto_details.html'
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
                "Você não tem permissão para visualizar este produto.")

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produto = context['data']

        context['details'] = {
            'Nome': produto.nome,
            'Descrição': produto.descricao,
            'Categoria': produto.categoria,
            'Unidade': produto.unidade_medida,
            'Quantidade em estoque': produto.quantidade_estoque,
            'Preço de custo': format_currency(produto.preco_custo),
            'Preço de venda': format_currency(produto.preco_venda),
            'Data de criação': format_date(produto.data_criacao),
            'Data de edição': format_date(produto.data_edicao),
            'Status': produto.get_status_display
        }
        context['update_url'] = f"/produto/editar/{produto.id}/"

        return context


@method_decorator(login_required, name='dispatch')
class ProdutoCreateView(CreateView):
    template_name = 'produto/produto_create.html'
    success_url = reverse_lazy('produto_list')

    def get_form_class(self):
        return ProdutoCreationAdminForm if self.request.user.is_superuser else ProdutoCreationFormBase

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

        create_produto(
            nome=form.cleaned_data['nome'],
            descricao=form.cleaned_data.get('descricao'),
            categoria=form.cleaned_data['categoria'],
            quantidade_inicial=form.cleaned_data.get(
                'quantidade_inicial') or 0,
            preco_custo=form.cleaned_data.get('preco_custo') or 0,
            preco_venda=form.cleaned_data.get('preco_venda') or 0,
            unidade_medida=form.cleaned_data['unidade_medida'],
            empresa=empresa,
            criado_por=usuario
        )

        messages.success(self.request, "Produto criado com sucesso!")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(
            self.request, "Por favor, corrija os erros abaixo.")
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class ProdutoUpdateView(UpdateView):
    model = Produto
    template_name = 'produto/produto_update.html'
    context_object_name = 'produto'
    form_class = ProdutoUpdateForm

    def get_object(self, queryset=None):
        usuario = self.request.user
        produto = super().get_object(queryset)

        if usuario.is_superuser:
            return produto

        usuario_empresa = get_usuario_empresa(
            usuario_id=usuario.id, empresa_id=produto.empresa.id)

        if not usuario_empresa:
            raise Http404("Você não tem permissão para editar este produto.")

        return produto

    def form_valid(self, form):
        produto = self.get_object()

        update_produto(
            produto_id=produto.id,
            nome=form.cleaned_data['nome'],
            descricao=form.cleaned_data.get('descricao'),
            categoria=form.cleaned_data['categoria'],
            preco_custo=form.cleaned_data['preco_custo'],
            preco_venda=form.cleaned_data['preco_venda'],
            status=form.cleaned_data.get('status')
        )

        messages.success(self.request, "Produto atualizado com sucesso!")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Por favor, corrija os erros abaixo.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('produto_details', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class ProdutoChangeStatus(View):
    def post(self, request, *args, **kwargs):
        produto = get_object_or_404(Produto, pk=kwargs['pk'])
        if produto.status == 'ativo':
            produto.status = 'inativo'
            messages.success(
                request, f'O produto "{produto.nome}" foi desativado com sucesso.')
        else:
            produto.status = 'ativo'
            messages.success(
                request, f'O produto "{produto.nome}" foi ativado com sucesso.')
        produto.save()
        return redirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', reverse_lazy('produto_list'))


@method_decorator(login_required, name='dispatch')
class ProdutoDeleteView(DeleteView):
    model = Produto
    template_name = "produtos/produto_confirm_delete.html"
    context_object_name = "produto"
    success_url = reverse_lazy("produto_list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        nome_produto = self.object.nome
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request, f'O produto "{nome_produto}" foi excluído com sucesso.')
            return response
        except Exception as e:
            messages.error(
                request, f'Ocorreu um erro ao excluir o produto "{nome_produto}".')
            return redirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class ProdutosPorEmpresaView(View):
    def get(self, request, *args, **kwargs):
        empresa_id = request.GET.get('empresa_id')
        produtos = Produto.objects.filter(
            empresa_id=empresa_id).values('id', 'nome')
        return JsonResponse(list(produtos), safe=False)
