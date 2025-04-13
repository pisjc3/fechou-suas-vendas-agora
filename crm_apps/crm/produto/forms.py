from django import forms
from .models import Produto
from crm_apps.crm.empresa.models import Empresa
from crm_apps.crm.categoria.models import Categoria
from crm_apps.common.util.formats import format_currency


class ProdutoCreationFormBase(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'categoria', 'quantidade_estoque']

    nome = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Digite o nome da categoria'}),
    )
    descricao = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Digite a descrição'}),
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Escolha a categoria",
        label="Categoria"
    )
    unidade_medida = forms.ChoiceField(
        choices=Produto.UnidadeMedida.choices,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Unidade de medida"
    )
    quantidade_estoque = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Informe o valor'}),
        label="Quantidade inicial em estoque",
        help_text="Opcional"
    )
    preco_custo = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(
            attrs={'placeholder': 'Informe o valor de custo'}),
        label="Preço inicial de Custo",
        help_text="Opcional"
    )
    preco_venda = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(
            attrs={'placeholder': 'Informe o valor de venda'}),
        label="Preço inicial de venda",
        help_text="Opcional"
    )


class ProdutoCreationAdminForm(ProdutoCreationFormBase):
    class Meta:
        model = Produto
        fields = ProdutoCreationFormBase.Meta.fields + ['empresa']

    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Escolha a empresa",
        label="Empresa"
    )


class ProdutoUpdateForm(ProdutoCreationFormBase):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'categoria',
                  'preco_venda', 'preco_custo', 'status']

    status = forms.ChoiceField(
        choices=Produto.Status.choices,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Status"
    )

    def __init__(self, *args, **kwargs):
        """remove campos não editáveis"""
        super().__init__(*args, **kwargs)
        self.fields.pop('quantidade_estoque', None)
