from django.http import HttpResponseForbidden


def superadmin_required(view_func):
    """
    Um decorador que garante que o usuário tenha permissões de superusuário.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Você não tem permissão para acessar essa página.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
