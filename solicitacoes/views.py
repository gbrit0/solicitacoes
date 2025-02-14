from django.utils import timezone
import pyodbc, os
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from solicitacoes.forms import SolicitacaoForm, ProductFormset, Solicitacao, ProdutosForm, Produto, RateioProdutoFormSet, SelecionarRateioForm
from solicitacoes.models import ConfiguracaoRateio
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.db import transaction
from django.http import JsonResponse
from decimal import Decimal

def editar_solicitacao(request, c1_num=None):
    if c1_num:
        solicitacao = get_object_or_404(Solicitacao, c1_num=c1_num)
        is_new = False
    else:
        solicitacao = Solicitacao()
        is_new = True
    
    # Configurar formsets
    ProdutoFormSet = inlineformset_factory(
        Solicitacao, Produto, form=ProdutosForm, extra=1, can_delete=True
    )
    
    if request.method == 'POST':
        form = SolicitacaoForm(request.POST, instance=solicitacao)
        formset_produtos = ProdutoFormSet(request.POST, instance=solicitacao)
        
        if form.is_valid() and formset_produtos.is_valid():
            with transaction.atomic():
                # Salvar solicitação
                solicitacao = form.save()
                
                # Salvar produtos
                produtos = formset_produtos.save(commit=False)
                for produto_form in formset_produtos:
                    if produto_form.is_valid() and not produto_form.cleaned_data.get('DELETE', False):
                        produto = produto_form.save(commit=False)
                        produto.c1_num = solicitacao
                        produto.save()
                        
                        # Processar formset de rateio para cada produto
                        if 'rateio_formset' in request.POST and str(produto.pk) in request.POST['rateio_formset']:
                            rateio_prefix = f"rateio_{produto.pk}"
                            rateio_formset = RateioProdutoFormSet(
                                request.POST,
                                prefix=rateio_prefix,
                                instance=produto
                            )
                            
                            if rateio_formset.is_valid():
                                # Verificar se o total de percentuais é 100%
                                total_percentual = sum(form.cleaned_data['percentual'] 
                                                      for form in rateio_formset 
                                                      if form.cleaned_data and not form.cleaned_data.get('DELETE', False))
                                
                                if abs(total_percentual - Decimal('100.00')) > Decimal('0.01'):
                                    # Tratar erro - os percentuais não somam 100%
                                    pass
                                else:
                                    rateios = rateio_formset.save(commit=False)
                                    for rateio in rateios:
                                        rateio.produto = produto
                                        rateio.save()
                                    
                                    # Processar exclusões
                                    for obj in rateio_formset.deleted_objects:
                                        obj.delete()
                
                # Remover produtos marcados para exclusão
                for obj in formset_produtos.deleted_objects:
                    obj.delete()
                
                return redirect('listar_solicitacoes')
    else:
        form = SolicitacaoForm(instance=solicitacao)
        formset_produtos = ProdutoFormSet(instance=solicitacao)
        selecionar_rateio_form = SelecionarRateioForm()
    
    # Preparar formsets de rateio para cada produto
    produtos_rateio_formsets = {}
    if not is_new:
        for produto in solicitacao.produto_set.all():
            rateio_formset = RateioProdutoFormSet(
                instance=produto,
                prefix=f"rateio_{produto.pk}"
            )
            produtos_rateio_formsets[produto.pk] = rateio_formset
    
    return render(request, 'editar_solicitacao.html', {
        'form': form,
        'formset_produtos': formset_produtos,
        'produtos_rateio_formsets': produtos_rateio_formsets,
        'selecionar_rateio_form': selecionar_rateio_form,
    })

# View para carregar configuração de rateio via AJAX
def carregar_configuracao_rateio(request):
    if request.method == 'POST' and request.is_ajax():
        config_id = request.POST.get('configuracao_id')
        produto_id = request.POST.get('produto_id')
        
        if config_id and produto_id:
            try:
                config = ConfiguracaoRateio.objects.get(id=config_id)
                itens_rateio = list(config.itens.all().values('centro_custo', 'percentual'))
                return JsonResponse({'status': 'success', 'itens': itens_rateio})
            except ConfiguracaoRateio.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Configuração não encontrada'})
    
    return JsonResponse({'status': 'error', 'message': 'Requisição inválida'})



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
                                
                                cursor.execute("""SELECT MAX(R_E_C_N_O_) + 1FROM SC1010 """)
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
                                
                                instance.c1_filent = '0101'
                                
                                print(f"instance.ctj_desc '{instance.ctj_desc}'")
                                
                                # insert = (
                                #     f"BEGIN TRY "
                                #         f"BEGIN TRANSACTION; "
                                #         f"INSERT INTO SC1010 WITH (TABLOCKX)"
                                #         f"(C1_FILIAL, C1_NUM, C1_ITEM, C1_DESCRI, C1_CC, C1_PRODUTO, "
                                #         f"C1_LOCAL, C1_QUANT, C1_EMISSAO, C1_UM, C1_FILENT, "
                                #         f"C1_DATPRF, C1_SOLICIT, C1_XOBMEMO, R_E_C_N_O_, C1_XSOLWEB)"
                                #         f"VALUES ( "
                                #             f"'{solicitacao_form.c1_filial}', "
                                #             f"'{solicitacao_form.c1_num}', "
                                #             f"'{instance.c1_item}', "
                                #             f"'{produto}', "
                                #             f"'{instance.c1_cc}', "
                                #             f"'{instance.c1_produto}', "
                                #             f"'{instance.c1_local}', "
                                #             f"'{instance.c1_quant}', "
                                #             f"'{str(solicitacao_form.c1_emissao).replace('-', '')[:8]}', "
                                #             f"'{instance.c1_um}', "
                                #             f"'{instance.c1_filent}', "
                                #             f"'{str(instance.c1_datprf).replace('-', '')}', "
                                #             f"'{solicitacao_form.c1_solicit}', "
                                #             f"CONVERT(VARBINARY(MAX), '{instance.c1_obs}'), "
                                #             f"'{instance.r_e_c_n_o}', "
                                #             f"'{solicitacao_form.user.cpf}'); "
                                        
                                #         f"COMMIT; "
                                #     f"END TRY "
                                #     f"BEGIN CATCH "
                                #         f"ROLLBACK;"
                                #         f"THROW; "
                                #     f"END CATCH; "
                                # )
                                
                                # cursor.execute((
                                #     # f"BEGIN TRY "
                                #     #     f"BEGIN TRANSACTION; "
                                #         f"INSERT INTO SC1010"
                                #         f"(C1_FILIAL, C1_NUM, C1_ITEM, C1_DESCRI, C1_CC, C1_PRODUTO, "
                                #         f"C1_LOCAL, C1_QUANT, C1_EMISSAO, C1_UM, C1_FILENT, "
                                #         f"C1_DATPRF, C1_SOLICIT, C1_XOBMEMO, R_E_C_N_O_, C1_XSOLWEB)"
                                #         f"VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CONVERT(VARBINARY(MAX), ?), ?, ? ); "
                                #     #     f"COMMIT; "
                                #     # f"END TRY "
                                #     # f"BEGIN CATCH "
                                #     #     f"ROLLBACK;"
                                #     #     f"THROW; "
                                #     # f"END CATCH; "
                                # ), (solicitacao_form.c1_filial, solicitacao_form.c1_num, instance.c1_item, produto, instance.c1_cc,
                                #     instance.c1_produto, instance.c1_local, instance.c1_quant, str(solicitacao_form.c1_emissao).replace('-', '')[:8],
                                #     instance.c1_um, instance.c1_filent, str(instance.c1_datprf).replace('-', ''), solicitacao_form.c1_solicit,
                                #     instance.c1_obs, instance.r_e_c_n_o, solicitacao_form.user.id))

                                instance.save()
                                # conexao.commit() # no sql já tem o commit, testar se insere normalmente
                            except pyodbc.Error as e:
                                erros.append({
                                    'produto': produto,
                                    'erro': e
                                })

                            
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
