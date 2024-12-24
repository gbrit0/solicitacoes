from django.shortcuts import render, redirect
from django.utils import timezone
import pyodbc, os
from django.contrib.auth.decorators import login_required

from solicitacoes.forms import SolicitacaoForm, ProductFormset


@login_required(login_url='login')
def criar_solicitacao(request):
    
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

         
         if formset.is_valid():
            instances = formset.save(commit=False)
            connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"

            with pyodbc.connect(connectionString) as conexao:
               with conexao.cursor() as cursor:
                  for num, instance in enumerate(instances):
                     print(f"num, instance {num, instance}")
                     instance.c1_item = f"{num+1:04d}"
                     cursor.execute(f"select MAX(B1_DESC) from SB1010 WHERE B1_COD = '{instance.c1_produto}' AND D_E_L_E_T_ <> '*' AND B1_MSBLQL = '2' AND B1_FILIAL = '01'")
                     instance.c1_descri = cursor.fetchall()[0][0]
                     cursor.execute(f"select MAX(B1_UM) from SB1010 WHERE B1_COD = '{instance.c1_produto}' AND D_E_L_E_T_ <> '*' AND B1_MSBLQL = '2' AND B1_FILIAL = '01'")
                     instance.c1_um =  cursor.fetchall()[0][0]
                     cursor.execute(f"select MAX(B1_LOCPAD) from SB1010 WHERE B1_COD = '{instance.c1_produto}' AND D_E_L_E_T_ <> '*' AND B1_MSBLQL = '2' AND B1_FILIAL = '01'")
                     instance.c1_local =  cursor.fetchall()[0][0]
                     instance.save()

                     produto = str(instance.c1_descri).replace("\n", " ").replace("\r", " ")[:30]  # substituindo caracteres especiais e 
                                                                                                   # limitando a 30 caracteres pois é o máximo que a sc1010
                                                                                                   # permite em c1_descri
                     insert = f"""INSERT INTO SC1010
                                 (C1_FILIAL, C1_NUM, C1_ITEM, C1_DESCRI, C1_CC, C1_PRODUTO, 
                                 C1_LOCAL, C1_QUANT, C1_EMISSAO, C1_DATPRF, C1_SOLICIT, C1_OBS, R_E_C_N_O_)
                                 VALUES ( '{solicitacao.c1_filial}', 
                                          '{solicitacao.c1_num}', 
                                          '{instance.c1_item}', 
                                          '{produto}', 
                                          '{solicitacao.c1_cc}', 
                                          '{instance.c1_produto}', 
                                          '{instance.c1_local}', 
                                          '{instance.c1_quant}', 
                                          '{str(solicitacao.c1_emissao).replace("-", "")[:8]}', 
                                          '{str(solicitacao.c1_datprf).replace("-", "")}', 
                                          '{solicitacao.c1_solicit}', 
                                          '{solicitacao.c1_obs}', 
                                          '{instance.r_e_c_n_o}')"""
                     
                     print(f"<---------- ITEM {num+1:04d} ----------->")
                     print(f"""solicitacao.c1_filial: {solicitacao.c1_filial}""")
                     print(f"""solicitacao.c1_num: {solicitacao.c1_num}""")
                     print(f"""instance.c1_item: {instance.c1_item}""")
                     print(f"""produto: {produto}""")
                     print(f"""solicitacao.c1_cc: {solicitacao.c1_cc}""")
                     print(f"""instance.c1_produto: {instance.c1_produto}""")
                     print(f"""instance.c1_local: {instance.c1_local}""")
                     print(f"""instance.c1_quant: {instance.c1_quant}""")
                     print(f"""str(solicitacao.c1_emissao).replace("-", "")[:8]: {str(solicitacao.c1_emissao).replace("-", "")[:8]}""")
                     print(f"""str(solicitacao.c1_datprf).replace("-", ""): {str(solicitacao.c1_datprf).replace("-", "")}""")
                     print(f"""solicitacao.c1_solicit: {solicitacao.c1_solicit}""")
                     print(f"""solicitacao.c1_obs: {solicitacao.c1_obs}""")
                     print(f"""instance.r_e_c_n_o: {instance.r_e_c_n_o}\n""")
                     cursor.execute(insert)
                     conexao.commit()
               
            return redirect('lista_solicitacoes')
   else:
      solicitacao_form = SolicitacaoForm()
      formset = ProductFormset()
   
   context = {
      'solicitacao_form': solicitacao_form,
      'formset': formset
   }
   
   return render(request, 'solicitacoes/criar_solicitacao.html', context)

