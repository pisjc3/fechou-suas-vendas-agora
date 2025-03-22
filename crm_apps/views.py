from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .decorators import superadmin_required


@method_decorator(login_required, name='dispatch')
@method_decorator(superadmin_required, name='dispatch')
class CustomUserCreationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/create_account.html'
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
