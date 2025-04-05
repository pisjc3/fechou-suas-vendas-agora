from django import forms
from .models import Produto
from crm_apps.crm.empresa.models import Empresa
from crm_apps.crm.categoria.models import Categoria


class ProdutoCreationFormBase(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'categoria']

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
        fields = ['nome', 'descricao', 'categoria', 'status']

    status = forms.ChoiceField(
        choices=Produto.Status.choices,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Status"
    )
