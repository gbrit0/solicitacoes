from django.utils import timezone

def sincronizar_delecoes_protheus():
    """
    Sincroniza as deleções entre o Protheus e o Django.
    """
    from solicitacoes.models import Produto
    from django.db import connections
    
    print(f"[{timezone.now()}] Iniciando sincronização de deleções...")
    
    # Exemplo de conexão com o banco do Protheus
    with connections['protheus'].cursor() as cursor:
        cursor.execute("SELECT top 50 R_E_C_N_O_ FROM tabela_protheus WHERE d_e_l_e_t_ = '*' order by R_E_C_N_O_ DESC")
        deletados_protheus = [row[0] for row in cursor.fetchall()]
        
        print(f"Encontrados {len(deletados_protheus)} registros deletados no Protheus")
        
        for recno in deletados_protheus:
            try:
                count = Produto.objects.filter(r_e_c_n_o=recno, is_deleted=False).update(is_deleted=True)
                if count > 0:
                    print(f"Atualizado produto {recno}")
            except Exception as e:
                print(f"Erro ao atualizar produto {recno}: {e}")
    
    print(f"[{timezone.now()}] Sincronização concluída")