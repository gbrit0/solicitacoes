from django.shortcuts import render
from home.forms import FiltroSolicitacaoForm
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Solicitacao, Produto, StatusPedido, StatusSC1


def calcular_status(solicitacao):
    status_sc1 = StatusSC1.objects.filter(C1_NUM=solicitacao.c1_num).first()
    if status_sc1:
        if status_sc1.C1_QUJE == 0 and (status_sc1.C1_COTACAO == '      ' or status_sc1.C1_COTACAO == 'IMPORT') and status_sc1.C1_APROV == 'B':
            return '<i class="fa-solid fa-circle text-dark"></i>' # Preto - Solicitação Bloqueada

    status_pedido = StatusPedido.objects.filter(C7_NUM=solicitacao.c1_num).first()
    if not status_pedido:
        return '<i class="fa-solid fa-circle indigo"></i>' # Roxo - Caso não pegue o status do pedido
         
    
    if status_pedido.C7_CONAPRO == 'R':
        return '<i class="fa-solid fa-circle-xmark text-danger"></i>'  # X vermelho - Rejeitado pelo aprovador
    elif status_pedido.C7_CONAPRO == 'B' and status_pedido.C7_QUJE < status_pedido.C7_QUANT:
        return '<i class="fa-solid fa-circle text-primary"></i>'  # Azul - Em aprovação
    elif status_pedido.C7_RESIDUO:
        return '<i class="fa-solid fa-circle text-secondary"></i>'  # Cinza - PC Eliminado por Resíduo
    elif status_pedido.C7_CONTRA and status_pedido.C7_RESIDUO:
        return '<i class="fa-solid fa-circle text-info"></i>'  # Ciano - Contrato
    elif status_pedido.C7_TIPO != '1':
        return '<i class="fa-solid fa-circle brown"></i>'  # Marrom - ???
    elif status_pedido.C7_QQTDACLA > 0:
        return '<i class="fa-solid fa-circle text-orange"></i>'  # Laranja - Em recebimento - pré-nota
    elif status_pedido.C7_QUJE >= status_pedido.C7_QUANT:
        return '<i class="fa-solid fa-circle text-danger"></i>'  # Vermelho - Recebido
    elif status_pedido.C7_QUJE != 0 and status_pedido.C7_QUJE < status_pedido.C7_QUANT:
        return '<i class="fa-solid fa-circle text-warning"></i>'  # Amarelo - Recebido parcialmente
    elif status_pedido.C7_QUJE == 0 and status_pedido.C7_QQTDACLA == 0:
        return '<i class="fa-solid fa-circle text-success"></i>'  # Verde - Pendente




@login_required(login_url='login')
def lista_solicitacoes(request):
    form = FiltroSolicitacaoForm(request.GET or None)
        
    # Verifica se é admin
    if request.user.role == 'admin':
        solicitacoes = Solicitacao.objects.all()
    else:
        solicitacoes = Solicitacao.objects.filter(user=request.user)
    
    solicitacoes = solicitacoes.prefetch_related('user').order_by('-c1_num')
    produtos = Produto.objects.all().order_by('-c1_num')
    
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

    solicitacoes_com_status = [
            {
                'solicitacao': s,
                'status': calcular_status(s)
            }
            for s in solicitacoes
        ]
   
    context = {
        'solicitacoes': solicitacoes_com_status,
        'form': form,
        'produtos': produtos
    }
    
    return render(request, 'home/index.html', context)

