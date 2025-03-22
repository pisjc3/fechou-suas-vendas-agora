from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

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
