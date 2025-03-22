from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from .forms import CustomUserCreationForm


@method_decorator(login_required, name='dispatch')
class CustomUserCreationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/create_account.html'
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
