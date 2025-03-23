from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.urls import reverse_lazy
from crm_apps.users.forms import CustomUserCreationForm, UserSettingsForm
from django.contrib.auth.forms import PasswordChangeForm
from crm_apps.crm.util.decorators import superadmin_required
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

User = get_user_model()


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(superadmin_required, name='dispatch')
class CustomUserCreationView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/create_account.html'
    success_url = '/'

    def form_valid(self, form):
        messages.success(self.request, "Usuário criado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Houve um erro ao criar usuário. Tente novamente.")
        return super().form_invalid(form)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


@method_decorator(login_required, name='dispatch')
class UserSettingsView(UpdateView):
    model = User
    form_class = UserSettingsForm
    template_name = 'accounts/settings.html'
    success_url = reverse_lazy('settings')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Dados atualizados com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Houve um erro ao atualizar os dados. Tente novamente.")
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('settings')

    def form_valid(self, form):
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Senha alterada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Houve um erro ao atualizar os dados. Tente novamente.")
        return super().form_invalid(form)
