from django.shortcuts import render
from .models import Solicitacao
from .forms import FiltroSolicitacaoForm

def lista_solicitacoes(request):
   # Cria o formulário com os dados GET
   form = FiltroSolicitacaoForm(request.GET or None)
   
   # Consulta base de solicitacoes
   solicitacoes = Solicitacao.objects.all().order_by('-id')
   
    # Verifica se o formulário é válido
   if form.is_valid():
      data_inicio = form.cleaned_data.get('data_inicio')
      data_fim = form.cleaned_data.get('data_fim')
      
      # Lógica de filtro
      if data_inicio and data_fim:
         solicitacoes = solicitacoes.filter(data_cadastro__range=[data_inicio, data_fim])
      elif data_inicio:
         solicitacoes = solicitacoes.filter(data_cadastro__gte=data_inicio)
      elif data_fim:
         solicitacoes = solicitacoes.filter(data_cadastro__lte=data_fim)
   else:
      solicitacoes = Solicitacao.objects.all().order_by('-id')
   
   # Contexto para o template
   context = {
      'solicitacoes': solicitacoes,
      'form': form
   }
   
   return render(request, 'home/lista_solicitacoes.html', context)

