from django.shortcuts import render
from home.forms import FiltroSolicitacaoForm
from django.contrib.auth.decorators import login_required
from solicitacoes.models import Solicitacao, Produto


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
   
   context = {
      'solicitacoes': solicitacoes,
      'form': form,
      'produtos': produtos
   }
   
   return render(request, 'home/index.html', context)

