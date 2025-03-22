from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Informações adicionais", {"fields": ("avatar",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informações adicionais", {"fields": ("avatar",)}),
    )


admin.site.register(User, CustomUserAdmin)
