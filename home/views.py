from django.shortcuts import render, redirect
from home.forms import FiltroSolicitacaoForm
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import SolicitacaoForm, CadastrarSolicitacaoForm
from solicitacoes.models import Solicitacao



def lista_solicitacoes(request):
   # Cria o formulário com os dados GET
   form = FiltroSolicitacaoForm(request.GET or None)
   
   # Consulta base de solicitacoes
   solicitacoes = Solicitacao.objects.all().order_by('-c1_datprf')
   
    # Verifica se o formulário é válido
   if form.is_valid():
      data_inicio = form.cleaned_data.get('data_inicio')
      data_fim = form.cleaned_data.get('data_fim')
      usuario = form.cleaned_data.get('usuario')
      
      # Lógica de filtro
      if data_inicio and data_fim:
         solicitacoes = solicitacoes.filter(data_cadastro__range=[data_inicio, data_fim])
      elif data_inicio:
         solicitacoes = solicitacoes.filter(data_cadastro__gte=data_inicio)
      elif data_fim:
         solicitacoes = solicitacoes.filter(data_cadastro__lte=data_fim)

      # Filtro de usuário
      if usuario:
         solicitacoes = solicitacoes.filter(user=usuario)

   else:
      solicitacoes = Solicitacao.objects.all().order_by('-c1_datprf')
   
   # Contexto para o template
   context = {
      'solicitacoes': solicitacoes,
      'form': form
   }
   
   return render(request, 'home/index.html', context)

def home(request):
   return render(request, 'home/index.html')


def cadastrar_solicitacao(request):
   form = CadastrarSolicitacaoForm(request.GET or None) 