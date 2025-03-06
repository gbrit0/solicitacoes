from django.shortcuts import render
from home.forms import FiltroSolicitacaoForm
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Solicitacao, Produto, StatusSC1 
from django.shortcuts import render
from setup.utils.sync import sincronizar_itens_deletados

def calcular_status(produto):
    status = StatusSC1.objects.filter(C1_NUM=produto.c1_num, C1_ITEM=produto.c1_item).first()
    
    if not status:
        return '<i class="fa-solid fa-circle text-secondary" data-bs-toggle="tooltip" title="Status Indefinido"></i>'

    # Mapeamento de status com ícones e cores
    status_mapping = [
        (status.C1_QUJE == 0 and status.C1_COTACAO in ['      ', 'IMPORT'] and status.C1_APROV == 'B', "#8A8A8A", "Solicitação Bloqueada", "fa-solid fa-circle"),
        (status.C1_QUJE == 0 and status.C1_COTACAO == '      ' and status.C1_APROV == 'L', "#98E45F", "Solicitação Pendente", "fa-solid fa-circle"),
        (status.C1_QUANT == status.C1_QUJE, "#D33434", "Solicitação Totalmente Atendida", "fa-solid fa-circle"),
        (status.C1_QUJE > 0 and status.C1_QUJE < status.C1_QUANT and status.C1_COTACAO == 'XXXXXX', "#FF0000", "Solicitação Parcialmente Atendida Utilizada em Cotação", "bi bi-triangle-fill"),
        (status.C1_QUJE > 0 and status.C1_QUJE < status.C1_QUANT, "#E7E720", "Solicitação Parcialmente Atendida", "fa-solid fa-circle"),
        (status.C1_COTACAO != '      ', "#4284C1", "Solicitação em Processo de Cotação", "fa-solid fa-circle"),
        (status.C1_RESIDUO == 'S', "#636363", "Elim. por Resíduo", "fa-solid fa-circle"),
        (status.C1_IMPORT == 'S', "#EB28DD", "Solicitação de Produto Importado", "fa-solid fa-circle"),
        (status.C1_QUJE == 0 and status.C1_COTACAO in ['      ', 'IMPORT'] and status.C1_APROV == 'R', "#ECA733", "Solicitação Rejeitada", "fa-solid fa-circle"),
        (status.C1_RESIDUO == 'S' and status.C1_COMPRAC == '1', "#6D1D6B", "Solicitação em Compra Centralizada", "fa-solid fa-circle")
    ]
    
    for condition, color, tooltip, icon in status_mapping:
        if condition:
            return f'<i class="{icon}" style="color: {color};" data-bs-toggle="tooltip" title="{tooltip}"></i>'
    
    return '<i class="fa-solid fa-circle text-secondary" data-bs-toggle="tooltip" title="Status Indefinido"></i>'

# def calcular_status(solicitacao):
#     status_sc1 = StatusSC1.objects.filter(C1_NUM=solicitacao.c1_num).first()
#     if status_sc1.C1_QUJE == 0 and (status_sc1.C1_COTACAO == '      ' or status_sc1.C1_COTACAO == 'IMPORT') and status_sc1.C1_APROV == 'B':
#         return '<i class="fa-solid fa-circle text-dark"  data-bs-toggle="tooltip" title="Solicitação Bloqueada"></i>' # Preto - Solicitação Bloqueada


#     status_pedido = StatusPedido.objects.filter(C7_NUMSC=solicitacao.c1_num).first()
    
#     if not status_pedido:
#         return '<i class="fa-solid fa-circle indigo"  data-bs-toggle="tooltip" title="Sem status"></i>' # Roxo - Caso não pegue o status do pedido
         
    
#     if status_pedido.C7_CONAPRO == 'R':
#         return '<i class="fa-solid fa-circle-xmark text-danger"  data-bs-toggle="tooltip" title="Rejeitado pelo aprovador"></i>'  # X vermelho - Rejeitado pelo aprovador
#     elif status_pedido.C7_CONAPRO == 'B' and status_pedido.C7_QUJE < status_pedido.C7_QUANT:
#         return '<i class="fa-solid fa-circle text-primary" data-bs-toggle="tooltip" title="Em aprovação"></i>'  # Azul - Em aprovação
#     elif status_pedido.C7_RESIDUO:
#         return '<i class="fa-solid fa-circle text-secondary" data-bs-toggle="tooltip" title="PC Eliminado por Resíduo"></i>'  # Cinza - PC Eliminado por Resíduo
#     elif status_pedido.C7_CONTRA and status_pedido.C7_RESIDUO:
#         return '<i class="fa-solid fa-circle text-info" data-bs-toggle="tooltip" title="Contrato"></i>'  # Ciano - Contrato
#     elif status_pedido.C7_TIPO != '1':
#         return '<i class="fa-solid fa-circle brown"></i>'  # Marrom - ???
#     elif status_pedido.C7_QQTDACLA > 0:
#         return '<i class="fa-solid fa-circle text-orange" data-bs-toggle="tooltip" title="Em recebimento"></i>'  # Laranja - Em recebimento - pré-nota
#     elif status_pedido.C7_QUJE >= status_pedido.C7_QUANT:
#         return '<i class="fa-solid fa-circle text-danger" data-bs-toggle="tooltip" title="Recebido"></i>'  # Vermelho - Recebido
#     elif status_pedido.C7_QUJE != 0 and status_pedido.C7_QUJE < status_pedido.C7_QUANT:
#         return '<i class="fa-solid fa-circle text-warning" data-bs-toggle="tooltip" title="Parcialmente Recebido"></i>'  # Amarelo - Recebido parcialmente
#     elif status_pedido.C7_QUJE == 0 and status_pedido.C7_QTDACLA == 0:
#         return '<i class="fa-solid fa-circle text-success" data-bs-toggle="tooltip" title="Pendente"></i>'  # Verde - Pendente




@login_required(login_url='login')
def lista_solicitacoes(request):
    sincronizar_itens_deletados()
    form = FiltroSolicitacaoForm(request.GET or None)
        
    # Verifica se é admin
    if request.user.role == 'admin':
        solicitacoes = Solicitacao.objects.all()
    else:
        solicitacoes = Solicitacao.objects.filter(user=request.user)
    
    solicitacoes = solicitacoes.prefetch_related('user').order_by('-c1_num')
    produtos = Produto.objects.filter(is_deleted=True).order_by('-c1_num')
    
    if form.is_valid():
        data_inicio = form.cleaned_data.get('data_inicio')
        data_fim = form.cleaned_data.get('data_fim')
        usuario = form.cleaned_data.get('usuario')
        
        if data_inicio and data_fim:
            solicitacoes = solicitacoes.filter(c1_emissao__range=[data_inicio, data_fim])
        elif data_inicio:
            solicitacoes = solicitacoes.filter(c1_emissao__gte=data_inicio)
        elif data_fim:
            solicitacoes = solicitacoes.filter(c1_emissao__lte=data_fim)

        # Filtro de usuário apenas para admin
        if usuario and request.user.role == 'admin':
            solicitacoes = solicitacoes.filter(user=usuario)

    
    solicitacoes_com_produtos = [
        {
            'solicitacao': s,
            'produtos': [
                {
                    'produto': p,
                    'status': calcular_status(p)
                }
                for p in Produto.objects.filter(c1_num=s, is_deleted=False)  # Filtrando produtos ativos
            ]
        }
        for s in solicitacoes
    ]

    context = {
        'solicitacoes': solicitacoes_com_produtos,
        'form': form,
    }
    return render(request, 'home/index.html', context)
