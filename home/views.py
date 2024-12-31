from django.shortcuts import render
from home.forms import FiltroSolicitacaoForm
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Solicitacao, Produto, StatusPedido


def calcular_status(solicitacao):
    status_pedido = StatusPedido.objects.filter(C7_NUM=solicitacao.c1_num).first()
    if not status_pedido:
        # return '<i class="fa-solid fa-circle text-secondary"></i>'  
        # return '<i class="text-danger fa-solid fa-circle-xmark">Rejeitado</i>'  # Rejeitado
        return '<i class="text-warning fa-solid fa-hourglass-half">Em aprovação</i>'  # Em aprovação
        return '<i class="text-danger fa-solid fa-trash">Eliminado</i>'  # Eliminado
        return '<i class="text-info fa-solid fa-file-contract">Contrato</i>'  # Contrato
        return '<i class="text-primary fa-solid fa-lock">Autorização</i>'  # Autorização
        return '<i class="text-info fa-solid fa-truck">Em recebimento</i>'  # Em recebimento
        return '<i class="text-success fa-solid fa-check-circle">Recebido</i>'  # Recebido
        return '<i class="text-warning fa-solid fa-circle-half-stroke">Parcial</i>'  # Parcial
        return '<i class="text-secondary fa-solid fa-clock">Pendente</i>'  # Pendente
         
    
    if status_pedido.C7_CONAPRO == 'R':
        return '<i class="text-danger fa-solid fa-circle-xmark"></i>'  # Rejeitado
    elif status_pedido.C7_CONAPRO == 'B' and status_pedido.C7_QUJE < status_pedido.C7_QUANT:
        return '<i class="text-warning fa-solid fa-hourglass-half"></i>'  # Em aprovação
    elif status_pedido.C7_RESIDUO:
        return '<i class="text-danger fa-solid fa-trash"></i>'  # Eliminado
    elif status_pedido.C7_CONTRA and status_pedido.C7_RESIDUO:
        return '<i class="text-info fa-solid fa-file-contract"></i>'  # Contrato
    elif status_pedido.C7_TIPO != '1':
        return '<i class="text-primary fa-solid fa-lock"></i>'  # Autorização
    elif status_pedido.C7_QQTDACLA > 0:
        return '<i class="text-info fa-solid fa-truck"></i>'  # Em recebimento
    elif status_pedido.C7_QUJE >= status_pedido.C7_QUANT:
        return '<i class="text-success fa-solid fa-check-circle"></i>'  # Recebido
    elif status_pedido.C7_QUJE > 0 and status_pedido.C7_QUJE < status_pedido.C7_QUANT:
        return '<i class="text-warning fa-solid fa-circle-half-stroke"></i>'  # Parcial
    elif status_pedido.C7_QUJE == 0 and status_pedido.C7_QQTDACLA == 0:
        return '<i class="text-secondary fa-solid fa-clock"></i>'  # Pendente
    return '<i class="text-secondary fa-solid fa-circle"></i>'  # Indefinido




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

