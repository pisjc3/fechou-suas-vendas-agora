from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.generic import TemplateView
from datetime import datetime, timedelta
from crm_apps.crm.cliente.models import Cliente
from crm_apps.crm.movimentacao.models import Movimentacao
from crm_apps.crm.util.selectors import get_empresa_do_usuario
from django.contrib import messages
from datetime import datetime, timedelta


@method_decorator(login_required, name='dispatch')
class AnalisarListView(TemplateView):
    template_name = 'analisar/analisar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        usuario = self.request.user
        is_superuser = usuario.is_superuser
        empresa = None

        empresa = get_empresa_do_usuario(usuario_id=usuario.id)
        if not empresa and not is_superuser:
            messages.error(
                self.request, "Você não tem uma empresa associada.")
            return

        # Dados para os gráficos iniciais (últimos 30 dias)
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=30)

        context['clientes_data'] = self.get_clientes_data(
            data_inicio, data_fim)
        context['movimentacoes_data'] = self.get_movimentacoes_data(
            data_inicio, data_fim)
        context['produtos_data'] = self.get_produtos_data(
            data_inicio, data_fim)
        context['vendas_por_cliente_data'] = self.get_vendas_por_cliente(
            data_inicio, data_fim)

        return context

    def get_clientes_data(self, data_inicio, data_fim):
        data_fim = datetime.combine(data_fim, datetime.max.time())

        clientes = Cliente.objects.filter(
            data_criacao__gt=data_inicio,
            data_criacao__lt=data_fim
        )

        clientes_por_dia = {}
        for cliente in clientes:
            dia = cliente.data_criacao.strftime('%d/%m/%Y')
            clientes_por_dia[dia] = clientes_por_dia.get(dia, 0) + 1

        return {
            'labels': list(clientes_por_dia.keys()),
            'values': list(clientes_por_dia.values())
        }

    def get_movimentacoes_data(self, data_inicio, data_fim):
        data_fim = datetime.combine(data_fim, datetime.max.time())

        movimentacoes = Movimentacao.objects.filter(
            data_criacao__gte=data_inicio,
            data_criacao__lte=data_fim
        )

        vendas_por_dia = {}
        compras_por_dia = {}

        for mov in movimentacoes:
            dia = mov.data_criacao.strftime('%d/%m/%Y')
            if mov.tipo == 'venda':
                vendas_por_dia[dia] = vendas_por_dia.get(dia, 0) + 1
            elif mov.tipo == 'compra':
                compras_por_dia[dia] = compras_por_dia.get(dia, 0) + 1

        # Para garantir que todos os dias existam, mesmo que zerados
        todos_os_dias = set(list(vendas_por_dia.keys()) +
                            list(compras_por_dia.keys()))
        todos_os_dias = sorted(
            todos_os_dias, key=lambda d: datetime.strptime(d, '%d/%m/%Y'))

        vendas = [vendas_por_dia.get(dia, 0) for dia in todos_os_dias]
        compras = [compras_por_dia.get(dia, 0) for dia in todos_os_dias]

        return {
            'labels': todos_os_dias,
            'vendas': vendas,
            'compras': compras
        }

    def get_produtos_data(self, data_inicio, data_fim):
        data_fim = datetime.combine(data_fim, datetime.max.time())

        movimentacoes = Movimentacao.objects.filter(
            data_criacao__gte=data_inicio,
            data_criacao__lte=data_fim
        )

        produtos_vendidos = {}
        produtos_comprados = {}

        for mov in movimentacoes:
            dia = mov.data_criacao.strftime('%d/%m/%Y')
            produto_nome = mov.produto.nome
            quantidade = mov.quantidade

            if quantidade is None or quantidade <= 0:
                continue

            if mov.tipo == 'venda':
                produtos_vendidos[produto_nome] = produtos_vendidos.get(
                    produto_nome, 0) + quantidade
            elif mov.tipo == 'compra':
                produtos_comprados[produto_nome] = produtos_comprados.get(
                    produto_nome, 0) + quantidade

        # Unir as chaves de produtos para garantir que todos os produtos apareçam
        produtos = set(produtos_vendidos.keys()).union(
            set(produtos_comprados.keys()))

        vendas = [float(produtos_vendidos.get(produto, 0))
                  for produto in produtos]
        compras = [float(produtos_comprados.get(produto, 0))
                   for produto in produtos]

        return {
            'labels': list(produtos),
            'vendas': vendas,
            'compras': compras
        }

    def get_vendas_por_cliente(self, data_inicio, data_fim):
        data_fim = datetime.combine(data_fim, datetime.max.time())

        movimentacoes = Movimentacao.objects.filter(
            data_criacao__gte=data_inicio, data_criacao__lte=data_fim)

        vendas_por_cliente = {}

        for mov in movimentacoes:
            if mov.tipo == 'venda':
                cliente_nome = "Não informado"
                if mov.cliente:
                    cliente_nome = mov.cliente.nome

                vendas_por_cliente[cliente_nome] = vendas_por_cliente.get(
                    cliente_nome, 0) + 1

        return {
            'labels': list(vendas_por_cliente.keys()),
            'values': list(vendas_por_cliente.values())
        }

    def get(self, request, *args, **kwargs):
        # Verificar se é uma requisição AJAX verificando o cabeçalho HTTP_X_REQUESTED_WITH
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            tipo = request.GET.get('tipo')
            data_inicio = request.GET.get('data_inicio')
            data_fim = request.GET.get('data_fim')

            if not data_inicio or not data_fim:
                return JsonResponse({'error': 'Datas de início e fim são obrigatórias.'}, status=400)

            try:
                data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
                data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
            except ValueError:
                return JsonResponse({'error': 'Formato de data inválido.'}, status=400)

            if tipo == 'cliente':
                dados = self.get_clientes_data(data_inicio_dt, data_fim_dt)
            elif tipo == 'movimentacao':
                dados = self.get_movimentacoes_data(
                    data_inicio_dt, data_fim_dt)
            elif tipo == 'produto':
                dados = self.get_produtos_data(data_inicio_dt, data_fim_dt)
            elif tipo == 'vendas_por_cliente':
                dados = self.get_vendas_por_cliente(
                    data_inicio_dt, data_fim_dt)
            else:
                return JsonResponse({'error': 'Tipo inválido.'}, status=400)

            return JsonResponse(dados)

        return super().get(request, *args, **kwargs)
