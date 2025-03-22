from django import forms
from .models import Empresa
from crm_apps.crm.util.validators import telefone_validator, cnpj_validator
from django.core.exceptions import ValidationError


class EmpresaCreationForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome', 'cnpj', 'endereco', 'telefone']

    nome = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Digite o nome da empresa'}),
    )
    cnpj = forms.CharField(
        label="CNPJ",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '00.000.000/0000-00'}),
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

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')

        if cnpj:
            if Empresa.objects.filter(cnpj=cnpj).exists():
                raise ValidationError(
                    'Já existe uma empresa cadastrada com este CNPJ.')

            if not cnpj_validator(cnpj):
                raise ValidationError('CNPJ inválido.')

        return cnpj
