from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib import messages
from .forms import VendaForm, CompraForm, VendaAdminForm, CompraAdminForm
from .models import Movimentacao
from .services import create_venda, create_compra
from crm_apps.crm.util.selectors import get_empresa_do_usuario


class VendaCreateView(CreateView):
    model = Movimentacao
    success_url = reverse_lazy('home')
    form_class = VendaForm
    template_name = 'movimentacao/venda_form.html'

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


class CompraCreateView(CreateView):
    model = Movimentacao
    success_url = reverse_lazy('home')
    template_name = 'movimentacao/compra_form.html'

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
