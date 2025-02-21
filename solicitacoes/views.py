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
                connectionString = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"
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
                        erros = []
                        for num, instance in enumerate(instances):
                            try:
                                
                                cursor.execute("""SELECT MAX(R_E_C_N_O_) + 1 FROM SC1010 """)
                                instance.r_e_c_n_o = cursor.fetchone()[0] 

                                instance.c1_num = solicitacao_form

                                instance.c1_item = f"{num+1:04d}"
                                
                                cursor.execute(f"select MAX(B1_DESC) from SB1010 WHERE B1_COD = '{instance.c1_produto}' AND D_E_L_E_T_ <> '*' AND B1_MSBLQL = '2' AND B1_FILIAL = '01'")
                                instance.c1_descri = cursor.fetchall()[0][0]

                                produto = str(instance.c1_descri).replace("\n", " ").replace("\r", " ")[:30]

                                cursor.execute(f"select MAX(B1_UM) from SB1010 WHERE B1_COD = '{instance.c1_produto}' AND D_E_L_E_T_ <> '*' AND B1_MSBLQL = '2' AND B1_FILIAL = '01'")
                                instance.c1_um =  cursor.fetchall()[0][0]

                                cursor.execute(f"select MAX(B1_LOCPAD) from SB1010 WHERE B1_COD = '{instance.c1_produto}' AND D_E_L_E_T_ <> '*' AND B1_MSBLQL = '2' AND B1_FILIAL = '01'")
                                instance.c1_local =  cursor.fetchall()[0][0]
                                
                                cursor.execute(f"SELECT MAX(B1_CONTA) from SB1010 WHERE B1_COD = '{instance.c1_produto}' AND D_E_L_E_T_ <> '*' AND B1_MSBLQL = '2' AND B1_FILIAL = '01'")
                                instance.b1_conta =  cursor.fetchall()[0][0]
                                
                                instance.c1_filent = '0101'

                                if instance.ctj_desc != '':
                                    instance.c1_cc = '                '
                                    cursor.execute(
                                        f"SELECT "
                                            f"CTJ_SEQUEN, "
                                            f"CTJ_PERCEN, "
                                            f"CTJ_CCD "
                                        f"FROM CTJ010 "
                                        f"WHERE CTJ_RATEIO = '{instance.ctj_desc}'"
                                    )

                                    rateios = cursor.fetchall()
                                    recno_rateio = -99999
                                    for rateio in rateios:
                                        if recno_rateio < 0:
                                            cursor.execute("""SELECT MAX(R_E_C_N_O_) + 1 FROM SCX010 """)
                                            recno_rateio = cursor.fetchone()[0]
                                        else:
                                            recno_rateio += 1

                                        cursor.execute(
                                            (
                                                f"INSERT INTO SCX010 "
                                                f"(CX_FILIAL, CX_SOLICIT, CX_ITEMSOL, CX_ITEM, CX_PERC, CX_CC, CX_CONTA, R_E_C_N_O_)"
                                                    f"VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                                            ), (str(instance.c1_filent), str(solicitacao_form.c1_num), str(instance.c1_item), str(rateio[0][1:]), str(rateio[1])[1:], str(rateio[2]), str(instance.b1_conta), str(recno_rateio))
                                        )
                                        
                                        conexao.commit()

                                # print(f"instance.ctj_desc '{instance.ctj_desc}'")
                                
                                cursor.execute((
                                    f"INSERT INTO SC1010"
                                    f"(C1_FILIAL, C1_NUM, C1_ITEM, C1_DESCRI, C1_CC, C1_PRODUTO, "
                                    f"C1_LOCAL, C1_QUANT, C1_EMISSAO, C1_UM, C1_FILENT, "
                                    f"C1_DATPRF, C1_SOLICIT, C1_XOBMEMO, R_E_C_N_O_, C1_XSOLWEB, "
                                    f"C1_QUJE, C1_COTACAO, C1_APROV)"
                                    f"VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CONVERT(VARBINARY(MAX), ?), ?, ?, 0, '      ', 'B' ); "
                                    
                                ), (solicitacao_form.c1_filial, solicitacao_form.c1_num, instance.c1_item, produto, instance.c1_cc,
                                    instance.c1_produto, instance.c1_local, instance.c1_quant, str(solicitacao_form.c1_emissao).replace('-', '')[:8],
                                    instance.c1_um, instance.c1_filent, str(instance.c1_datprf).replace('-', ''), solicitacao_form.c1_solicit,
                                    instance.c1_obs, instance.r_e_c_n_o, solicitacao_form.user.id))

                            except pyodbc.Error as e:
                                erros.append({
                                    'produto': produto,
                                    'erro': e
                                })
                            else:
                                instance.save()
                                conexao.commit() 

                if erros:
                    for erro in erros:
                        messages.error(request, f"Não foi possível cadastrar a solicitação para o produto {erro['produto']}. Tente novamente mais tarde. ERRO: {erro['erro']}")
                else:
                    messages.success(request, "Solicitação cadastrada com sucesso!")
                            
                return redirect('lista_solicitacoes')
                
            except Exception as e:
                messages.error(request, f"Erro ao criar solicitação, por favor contate o admnistrador. ERRO: {e}")
                return redirect('lista_solicitacoes')
            
        else:
            return render(request, 'solicitacoes/criar_solicitacao.html', {
                'solicitacao_form': solicitacao_form,
                'formset': formset,
                'errors': formset.errors
            })
    
    solicitacao_form = SolicitacaoForm()
    formset = ProductFormset()
    return render(request, 'solicitacoes/criar_solicitacao.html', {
        'solicitacao_form': solicitacao_form,
        'formset': formset
    })


@login_required(login_url='login')
def apagar_solicitacao(request, num_solicitacao):
    if request.method == 'POST':
        # Adicione no início da função
        try:
            connectionString = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"
            
            with pyodbc.connect(connectionString) as conexao:
                with conexao.cursor() as cursor:
                    # Verifica se a solicitação existe e pertence ao usuário
                    cursor.execute("""
                        SELECT C1_NUM, C1_XSOLWEB 
                        FROM SC1010 
                        WHERE C1_NUM = ? 
                        AND D_E_L_E_T_ <> '*'
                    """, (num_solicitacao,))
                    
                    solicitacao = cursor.fetchone()
                
                    if not solicitacao:
                        messages.error(request, "Solicitação não encontrada.")
                        return redirect('lista_solicitacoes')
                    
                    if solicitacao.c1_aprov != 'B':
                        messages.error(request, "Solicitação já processada, não pode ser excluída")
                        return redirect('lista_solicitacoes')
                
                    # Verifica se o usuário tem permissão (é o criador da solicitação)
                    if str(solicitacao[1]) != str(request.user.id):
                        messages.error(request, "Você não tem permissão para apagar esta solicitação.")
                        return redirect('lista_solicitacoes')
                    
                    # Apaga os rateios relacionados
                    cursor.execute("""
                        DELETE FROM SCX010 
                        WHERE CX_SOLICIT = ?
                    """, (num_solicitacao,))
                    
                    # Apaga a solicitação principal e seus itens
                    cursor.execute("""
                        UPDATE SC1010 
                        SET D_E_L_E_T_ = '*'
                        WHERE C1_NUM = ?
                    """, (num_solicitacao,))
                    
                    conexao.commit()
                    
                    messages.success(request, "Solicitação apagada com sucesso!")
                    return redirect('lista_solicitacoes')
                    
        except pyodbc.Error as e:
            messages.error(request, f"Erro ao apagar solicitação. Por favor, contate o administrador. ERRO: {e}")
            return redirect('lista_solicitacoes')
    
    # Se for GET, mostra uma página de confirmação
    return render(request, 'solicitacoes/confirmar_exclusao.html', {
        'num_solicitacao': num_solicitacao
    })