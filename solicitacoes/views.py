from django.shortcuts import render, redirect
from django.forms import ModelForm
from .models import Produto, Solicitacao
from django.forms import inlineformset_factory
from django.utils import timezone
import pyodbc, os

def index(request, id_solicitacao):
   solicitacao = Solicitacao.objects.get(c1_num=id_solicitacao)
    
   ProductFormset = inlineformset_factory(
      Solicitacao,
      Produto,
      fields=('c1_produto', 'c1_descri', 'c1_um', 'c1_local', 'c1_quant')
   )
    
   if request.method == 'POST':
      formset = ProductFormset(
         request.POST, 
         instance=solicitacao
      )
      
      if formset.is_valid():
         instances = formset.save(commit=False)
         
         # Pega o último número de item para esta solicitação
         ultimo_item = Produto.objects.filter(
               c1_num=solicitacao
         ).order_by('-c1_item').first()
         
         # Define o número inicial
         if ultimo_item:
               proximo_num = int(ultimo_item.c1_item) + 1
         else:
               proximo_num = 1
               
         for instance in instances:
               # Gera o c1_item com 4 dígitos (exemplo: 0001, 0002, etc)
               instance.c1_item = f"{proximo_num:04d}"
               instance.c1_num = solicitacao
               instance.save()
               proximo_num += 1
         
         formset.save()
         return redirect('index', id_solicitacao=id_solicitacao)
   
   formset = ProductFormset(
         instance=solicitacao
      )
   
   context = {
      'formset': formset,
      'solicitacao': solicitacao
   }
   
   return render(request, 'home/login.html', context)

class SolicitacaoForm(ModelForm):
    class Meta:
        model = Solicitacao
        fields = ['c1_cc', 'c1_datprf']  # Apenas campos editáveis

def criar_solicitacao(request):
    ProductFormset = inlineformset_factory(
        Solicitacao,
        Produto,
        fields=('c1_produto', 'c1_descri', 'c1_um', 'c1_local', 'c1_quant'),
        extra=1,
        can_delete=True
    )
    
    if request.method == 'POST':
        solicitacao_form = SolicitacaoForm(request.POST)
        
        if solicitacao_form.is_valid():
            # Cria a solicitação sem salvar ainda
            solicitacao = solicitacao_form.save(commit=False)
            
            # Preenche os campos automáticos
            solicitacao.c1_filial = '0101'
            solicitacao.c1_user = '000000'
            solicitacao.c1_emissao = timezone.now()
            solicitacao.user = request.user
            
            connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"

            with pyodbc.connect(connectionString) as conexao:
               with conexao.cursor() as cursor:
                  cursor.execute("""SELECT 
                                       MAX(CONVERT(INT, C1_NUM))
                                    FROM SC1010
                                    WHERE TRIM(C1_NUM) NOT LIKE '%G%' 
                                    AND C1_NUM <> '""'
                                 """)
                  ultimo_num = cursor.fetchall()
            if ultimo_num:
               proximo_num = str(int(ultimo_num.c1_num) + 1).zfill(6)
            else:
               proximo_num = '000001'
            
            

            solicitacao.c1_num = proximo_num
            solicitacao.save()
            
            # Agora trata o formset dos produtos
            formset = ProductFormset(request.POST, instance=solicitacao)
            
            if formset.is_valid():
                instances = formset.save(commit=False)
                
                for num, instance in enumerate(instances, start=1):
                    instance.c1_item = f"{num:04d}"
                    instance.save()
                
                return redirect('index', id_solicitacao=solicitacao.c1_num)
    else:
        solicitacao_form = SolicitacaoForm()
        formset = ProductFormset()
    
    context = {
        'solicitacao_form': solicitacao_form,
        'formset': formset
    }
    
    return render(request, 'solicitacoes/criar_solicitacao.html', context)