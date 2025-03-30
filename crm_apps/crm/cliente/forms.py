from django import forms
from .models import Cliente
from crm_apps.common.validators import telefone_validator
from crm_apps.crm.empresa.models import Empresa


class ClienteCreationFormBase(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'endereco', 'telefone']

    nome = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Digite o nome do cliente'}),
    )
    endereco = forms.CharField(
        label="Endereço",
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Rua, Bairro, Cidade - CEP'}),
    )
    telefone = forms.CharField(
        validators=[telefone_validator],
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': '(DD) 99999-9999'}))


class ClienteCreationAdminForm(ClienteCreationFormBase):
    class Meta:
        model = Cliente
        fields = ClienteCreationFormBase.Meta.fields + ['empresa']

    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(),
        required=True,
        widget=forms.Select(),
        label="Empresa"
    )
