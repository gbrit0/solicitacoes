from django.utils import timezone
import pyodbc, os
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from solicitacoes.forms import SolicitacaoForm, ProductFormset
from django.shortcuts import render, redirect



@login_required(login_url='login')
def criar_solicitacao(request):
    if request.method == 'POST':
        solicitacao_form = SolicitacaoForm()
        formset = ProductFormset(request.POST)
        
        if formset.is_valid():
            try:
                solicitacao_form = solicitacao_form.save(commit=False)
                solicitacao_form.c1_filial = '0101'
                solicitacao_form.c1_solicit = '000000'
                solicitacao_form.c1_emissao = timezone.now()
                solicitacao_form.user = request.user
                solicitacao_form.tipo = 'Compra'
        
                # Busca próximo número
                connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"
                with pyodbc.connect(connectionString) as conexao:
                    with conexao.cursor() as cursor:
                        cursor.execute("""
                            SELECT MAX(CONVERT(INT, C1_NUM))
                            FROM SC1010
                            WHERE C1_NUM <> ''
                            AND TRIM(C1_NUM) NOT LIKE '%G%'
                            AND C1_NUM LIKE '[0-9]%';

                        """)
                        ultimo_num = cursor.fetchall()
                        
                proximo_num = str(int(ultimo_num[0][0]) + 1).zfill(6) if ultimo_num else '000001'
                solicitacao_form.c1_num = proximo_num
                solicitacao_form.save()

                instances = formset.save(commit=False)

                with pyodbc.connect(connectionString) as conexao:
                    with conexao.cursor() as cursor:
                        for num, instance in enumerate(instances):
                            # Atualiza dados do produto
                            instance.c1_num = solicitacao_form

                            instance.c1_item = f"{num+1:04d}"
                            produto = str(instance.c1_descri).replace("\n", " ").replace("\r", " ")[:30]
                            
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
                                            VALUES ( '{solicitacao_form.c1_filial}', 
                                                    '{solicitacao_form.c1_num}', 
                                                    '{instance.c1_item}', 
                                                    '{produto}', 
                                                    '{instance.c1_cc}', 
                                                    '{instance.c1_produto}', 
                                                    '{instance.c1_local}', 
                                                    '{instance.c1_quant}', 
                                                    '{str(solicitacao_form.c1_emissao).replace("-", "")[:8]}', 
                                                    '{str(instance.c1_datprf).replace("-", "")}', 
                                                    '{solicitacao_form.c1_solicit}', 
                                                    '{instance.c1_obs}', 
                                                    '{instance.r_e_c_n_o}')"""

                            cursor.execute(insert)
                            conexao.commit()
                            
                messages.success(request, "Solicitação criada com sucesso!")
                return redirect('lista_solicitacoes')  # Adicione esta URL nas suas urls.py
                
            except Exception as e:
                # messages.error(request, f"Erro ao criar solicitação: {str(e)}")
                # return render(request, 'solicitacoes/criar_solicitacao.html', {
                #     'solicitacao_form': solicitacao_form,
                #     'formset': formset
                # })
                raise e
    

    solicitacao_form = SolicitacaoForm()
    formset = ProductFormset()
    return render(request, 'solicitacoes/criar_solicitacao.html', {
        'solicitacao_form': solicitacao_form,
        'formset': formset
    })
