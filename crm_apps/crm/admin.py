
from crm_apps.crm.usuario_empresa.models import UsuarioEmpresa
from crm_apps.crm.empresa.models import Empresa
from django.contrib import admin


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cnpj', 'endereco', 'telefone', 'criado_por')
    search_fields = ('nome', 'cnpj', 'endereco', 'telefone', 'criado_por')
    ordering = ('-id',)


@admin.register(UsuarioEmpresa)
class UsuarioEmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'empresa')
    search_fields = ('usuario', 'empresa')
    ordering = ('-id',)
