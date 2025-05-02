from django import forms
from .models import Movimentacao
from crm_apps.crm.produto.models import Produto
from crm_apps.crm.cliente.models import Cliente
from crm_apps.crm.empresa.models import Empresa
from crm_apps.crm.util.selectors import get_empresa_do_usuario


class MovimentacaoFormBase(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = [
            'produto',
            'quantidade',
        ]

    produto = forms.ModelChoiceField(
        queryset=Produto.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Produto',
        empty_label='Selecione o produto'
    )

    quantidade = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Informe a quantidade',
            'min': 0,
        }),
        label='Quantidade'
    )


class VendaForm(MovimentacaoFormBase):
    class Meta(MovimentacaoFormBase.Meta):
        fields = MovimentacaoFormBase.Meta.fields + [
            'cliente',
            'preco_unitario'
        ]

    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Cliente',
        empty_label="Selecione o cliente"
    )
    preco_unitario = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Informe o preço unitário desta venda'
        }),
        label='Preço unitário'
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            usuario = request.user
            if usuario.is_superuser:
                self.fields['produto'].queryset = Produto.objects.filter(
                    status='ativo'
                )
                self.fields['cliente'].queryset = Cliente.objects.all()
                return
            empresa = get_empresa_do_usuario(usuario_id=usuario.id)
            if empresa:
                self.fields['produto'].queryset = Produto.objects.filter(
                    status='ativo',
                    empresa=empresa
                )
                self.fields['cliente'].queryset = Cliente.objects.filter(
                    empresa=empresa)


class CompraForm(MovimentacaoFormBase):
    class Meta(MovimentacaoFormBase.Meta):
        fields = MovimentacaoFormBase.Meta.fields + [
            'novo_preco_custo',
            'novo_preco_venda',
        ]

    novo_preco_custo = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Novo preço de custo',
            'min': 0
        }),
        label='Novo preço de custo (R$)'
    )

    novo_preco_venda = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Novo preço de venda',
            'min': 0
        }),
        label='Novo preço de venda (R$)'
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            usuario = request.user
            if usuario.is_superuser:
                self.fields['produto'].queryset = Produto.objects.filter(
                    status='ativo'
                )
                return
            empresa = get_empresa_do_usuario(usuario_id=usuario.id)
            if empresa:
                self.fields['produto'].queryset = Produto.objects.filter(
                    status='ativo',
                    empresa=empresa
                )


class VendaAdminForm(VendaForm):
    class Meta(VendaForm.Meta):
        fields = ['empresa'] + VendaForm.Meta.fields

    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Empresa",
        empty_label="Selecione a empresa",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        data = kwargs.get('data', {})
        empresa_id = data.get('empresa') if data.get(
            'empresa') else self.initial.get('empresa')

        if empresa_id:
            self.fields['produto'].queryset = Produto.objects.filter(
                empresa_id=empresa_id)
            self.fields['cliente'].queryset = Cliente.objects.filter(
                empresa_id=empresa_id)
        else:
            self.fields['produto'].queryset = Produto.objects.none()
            self.fields['cliente'].queryset = Cliente.objects.none()


class CompraAdminForm(CompraForm):
    class Meta(CompraForm.Meta):
        fields = ['empresa'] + CompraForm.Meta.fields

    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Empresa",
        empty_label="Selecione a empresa",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        data = kwargs.get('data', {})
        empresa_id = data.get('empresa') if data.get(
            'empresa') else self.initial.get('empresa')

        if empresa_id:
            self.fields['produto'].queryset = Produto.objects.filter(
                empresa_id=empresa_id)
        else:
            self.fields['produto'].queryset = Produto.objects.none()
