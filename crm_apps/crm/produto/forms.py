from django import forms
from .models import Produto
from crm_apps.crm.empresa.models import Empresa
from crm_apps.crm.categoria.models import Categoria
from crm_apps.crm.util.selectors import get_empresa_do_usuario


class ProdutoCreationFormBase(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'categoria',
                  'unidade_medida', 'quantidade_estoque']

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
        queryset=Categoria.objects.none(),
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
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Informe a quantidade',
                'min': 0,
            }
        ),
        label="Quantidade inicial em estoque",
    )
    preco_custo = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(
            attrs={'placeholder': 'Informe o valor de custo', 'min': 0}),
        label="Preço inicial de Custo (R$)",
    )
    preco_venda = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(
            attrs={'placeholder': 'Informe o valor de venda', 'min': 0}),
        label="Preço inicial de venda (R$)",
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            usuario = request.user
            if usuario.is_superuser:
                self.fields['categoria'].queryset = Categoria.objects.all()
                return
            empresa = get_empresa_do_usuario(usuario_id=usuario.id)
            if empresa:
                self.fields['categoria'].queryset = Categoria.objects.filter(
                    empresa=empresa
                )


class ProdutoCreationAdminForm(ProdutoCreationFormBase):
    class Meta:
        model = Produto
        fields = ['empresa'] + ProdutoCreationFormBase.Meta.fields

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
        fields = ['nome', 'descricao', 'categoria', 'unidade_medida',
                  'preco_custo', 'preco_venda', 'status']

    status = forms.ChoiceField(
        choices=Produto.Status.choices,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Status"
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['preco_custo'].label = "Novo preço de Custo (R$)"
        self.fields['preco_venda'].label = "Novo preço de Venda (R$)"

        """remove campos não editáveis"""
        self.fields.pop('quantidade_estoque', None)

        produto_instance = self.instance

        if request:
            usuario = request.user
            if usuario.is_superuser:
                self.fields['categoria'].queryset = Categoria.objects.filter(
                    empresa_id=produto_instance.empresa.id)
                return
            empresa = get_empresa_do_usuario(usuario_id=usuario.id)
            if empresa:
                self.fields['categoria'].queryset = Categoria.objects.filter(
                    empresa=empresa
                )
