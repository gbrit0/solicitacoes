from django.db import transaction
import pyodbc
import os
from solicitacoes.models import Produto

def sincronizar_itens_deletados():
   connectionString = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"
   
   conexao = pyodbc.connect(connectionString)

   cursor = conexao.cursor()

   query = """
   SELECT TOP 50 C1_NUM, C1_ITEM
   FROM SC1010
   WHERE D_E_L_E_T_ = '*'
   ORDER BY R_E_C_N_O_ DESC
   """
   cursor.execute(query)
   
   itens_deletados = cursor.fetchall()

   if not itens_deletados:
      print("Nenhum item deletado encontrado no Protheus.")
      return

   with transaction.atomic():
      for c1_num, c1_item in itens_deletados:
         Produto.objects.filter(c1_num=c1_num, c1_item=c1_item).update(is_deleted=True)

   print(f"{len(itens_deletados)} produtos marcados como deletados.")

   cursor.close()
   conexao.close()



