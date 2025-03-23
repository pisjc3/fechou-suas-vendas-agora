from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import CustomLoginView, CustomUserCreationView, CustomPasswordResetView, UserSettingsView, CustomPasswordChangeView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('configuracoes/', UserSettingsView.as_view(), name='settings'),
    path('alterar_senha/', CustomPasswordChangeView.as_view(),
         name='password_change'),
    path('criar_conta/',
         CustomUserCreationView.as_view(), name='create_account'),
    path('resetar_senha/',
         CustomPasswordResetView.as_view(), name='password_reset'),
    path('resetar_senha/done/',
         PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('resetar_senha/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('resetar_senha/complete/',
         PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
