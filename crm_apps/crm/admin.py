
from crm_apps.crm.usuario_empresa.models import UsuarioEmpresa
from crm_apps.crm.empresa.models import Empresa
from crm_apps.crm.cliente.models import Cliente
from crm_apps.crm.categoria.models import Categoria
from crm_apps.crm.produto.models import Produto
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


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'endereco',
                    'telefone', 'empresa', 'criado_por')
    search_fields = ('nome', 'empresa')
    ordering = ('-id',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'descricao', 'empresa', 'criado_por')
    search_fields = ('nome', 'descricao', 'empresa')
    ordering = ('-id',)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'descricao',
                    'categoria', 'empresa', 'criado_por', 'status')
    search_fields = ('nome', 'descricao', 'categoria', 'empresa')
    ordering = ('-id',)
