from django import forms
from .models import Categoria
from crm_apps.crm.empresa.models import Empresa


class CategoriaCreationFormBase(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']

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


class CategoriaCreationAdminForm(CategoriaCreationFormBase):
    class Meta:
        model = Categoria
        fields = CategoriaCreationFormBase.Meta.fields + ['empresa']

    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(),
        required=True,
        widget=forms.Select(),
        label="Empresa"
    )


class CategoriaUpdateForm(CategoriaCreationFormBase):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
