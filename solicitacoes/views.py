from django.shortcuts import render
from django import forms
from django.utils import timezone
import pyodbc, os
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from solicitacoes.forms import SolicitacaoForm, ProductFormset
from django.forms import ValidationError


@login_required(login_url='login')
def criar_solicitacao(request):
   solicitacao_form = SolicitacaoForm()
   formset = ProductFormset()
      
   context = {
      'solicitacao_form': solicitacao_form,
      'formset': formset
   }
   if request.method == 'POST':
      solicitacao_form = SolicitacaoForm(request.POST)
      
      formset = ProductFormset(request.POST)
      
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
            proximo_num = str(int(ultimo_num[0][0]) + 1).zfill(6)
         else:
            proximo_num = '000001'
         
         

         solicitacao.c1_num = proximo_num
         
         solicitacao.save()

         # Agora trata o formset dos produtos
         formset = ProductFormset(request.POST, instance=solicitacao)

         try:
            if not formset.is_valid():
               errors = []
               for form in formset:
                  if form.errors:
                     errors.append(form.errors)
               messages.error(request, f"Por favor, corrija os erros no formulário!")
               return render(request, 'solicitacoes/criar_solicitacao.html', {
                  'solicitacao_form': solicitacao_form,
                  'formset': formset
               })
            else:
                  
               instances = formset.save(commit=False)
               connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"

               with pyodbc.connect(connectionString) as conexao:
                  with conexao.cursor() as cursor:
                        for num, instance in enumerate(instances):
                           produto = str(instance.c1_descri).replace("\n", " ").replace("\r", " ")[:30]
                           print(f"solicitacao.c1_filial {solicitacao.c1_filial}")
                           print(f"solicitacao.c1_num {solicitacao.c1_num}")
                           print(f"instance.c1_item {instance.c1_item}")
                           print(f"produto {produto}")
                           print(f"instance.c1_cc {instance.c1_cc}")
                           print(f"instance.c1_produto {instance.c1_produto}")
                           print(f"instance.c1_local {instance.c1_local}")
                           print(f"instance.c1_quant {instance.c1_quant}")
                           print(f"solicitacao.c1_emissao {solicitacao.c1_emissao}")
                           print(f"instance.c1_datprf {instance.c1_datprf}")
                           print(f"solicitacao.c1_solicit {solicitacao.c1_solicit}")
                           print(f"instance.c1_obs {instance.c1_obs}")
                           print(f"instance.r_e_c_n_o {instance.r_e_c_n_o}")
                           print(f"user {solicitacao.user.cpf}")

                           instance.c1_item = f"{num+1:04d}"
                           cursor.execute(f"select MAX(B1_DESC) from SB1010 WHERE B1_COD = '{instance.c1_produto}' AND D_E_L_E_T_ <> '*' AND B1_MSBLQL = '2' AND B1_FILIAL = '01'")
                           
                           instance.c1_descri = cursor.fetchall()[0][0]
                           cursor.execute(f"select MAX(B1_UM) from SB1010 WHERE B1_COD = '{instance.c1_produto}' AND D_E_L_E_T_ <> '*' AND B1_MSBLQL = '2' AND B1_FILIAL = '01'")
                           
                           instance.c1_um =  cursor.fetchall()[0][0]
                           cursor.execute(f"select MAX(B1_LOCPAD) from SB1010 WHERE B1_COD = '{instance.c1_produto}' AND D_E_L_E_T_ <> '*' AND B1_MSBLQL = '2' AND B1_FILIAL = '01'")
                           
                           instance.c1_local =  cursor.fetchall()[0][0]
                           instance.save()

                           insert = f"""INSERT INTO SC1010
                                       (C1_FILIAL, C1_NUM, C1_ITEM, C1_DESCRI, C1_CC, C1_PRODUTO, 
                                       C1_LOCAL, C1_QUANT, C1_EMISSAO, C1_DATPRF, C1_SOLICIT, C1_OBS, R_E_C_N_O_)
                                       VALUES ( '{solicitacao.c1_filial}', 
                                                '{solicitacao.c1_num}', 
                                                '{instance.c1_item}', 
                                                '{produto}', 
                                                '{instance.c1_cc}', 
                                                '{instance.c1_produto}', 
                                                '{instance.c1_local}', 
                                                '{instance.c1_quant}', 
                                                '{str(solicitacao.c1_emissao).replace("-", "")[:8]}', 
                                                '{str(instance.c1_datprf).replace("-", "")}', 
                                                '{solicitacao.c1_solicit}', 
                                                '{instance.c1_obs}', 
                                                '{instance.r_e_c_n_o}')"""

                           cursor.execute(insert)
                           conexao.commit()

         except ValueError as e:
            # Pega os erros do formset para logging e feedback ao usuário
            errors = []
            for form in formset:
               if form.errors:
                  raise forms.ValidationError(f"Campos obrigatórios")
            print(f"Erros no formset: {errors}")
            raise  # Re-levanta a exceção para ser tratada pela view
         except Exception as e:
            print(f"Erro inesperado: {str(e)}")
            raise  # Re-levanta a exceção para ser tratada pela view
                     
   else:
      solicitacao_form = SolicitacaoForm()
      formset = ProductFormset()
   
   context = {
      'solicitacao_form': solicitacao_form,
      'formset': formset
   }
   
   return render(request, 'solicitacoes/criar_solicitacao.html', context)

