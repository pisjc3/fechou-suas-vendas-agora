from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from crm_apps.crm.usuario_empresa.models import UsuarioEmpresa
from crm_apps.crm.empresa.models import Empresa


class CustomUserCreationForm(UserCreationForm):
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(), required=True, label='Empresa')

    class Meta:
        model = User
        fields = ['username', 'password1',
                  'password2', 'email', 'empresa']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password1'].error_messages = {
            'required': 'Este campo é obrigatório.',
            'invalid': 'Senha inválida.'
        }
        self.fields['password2'].help_text = None
        self.fields['password2'].error_messages = {
            'required': 'Este campo é obrigatório.',
            'invalid': 'As senhas não coincidem.'
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        empresa = self.cleaned_data.get('empresa')
        UsuarioEmpresa.objects.create(usuario=user, empresa=empresa)

        return user
