from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from crm_apps.crm.empresa.models import Empresa
from crm_apps.crm.usuario_empresa.models import UsuarioEmpresa
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(), required=True, label='Empresa')
    avatar = forms.ImageField(required=False, label="Avatar")

    class Meta:
        model = User
        fields = ['username', 'password1',
                  'password2', 'email', 'avatar', 'empresa']

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

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        empresa = self.cleaned_data.get('empresa')
        UsuarioEmpresa.objects.create(usuario=user, empresa=empresa)

        return user
