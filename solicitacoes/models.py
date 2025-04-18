from django.db import models
from django.contrib.auth import get_user_model 

User = get_user_model()

class Solicitacao(models.Model):
   c1_filial = models.CharField(max_length=4, null=False, default='0101') # '0101'
   c1_num = models.CharField(max_length=6, null=False, default='', primary_key=True) # max(sc1)
   c1_solicit = models.CharField(max_length=6, null=False, default='000000')
   c1_emissao = models.DateField(blank=False)
   user = models.ForeignKey(User, to_field='cpf', default='', on_delete=models.DO_NOTHING)
   tipo = models.CharField(max_length=15, null=False, default='Compra')
   status = models.CharField(max_length=30, default='')

   def __str__(self):
      return str(self.c1_num)
   
class Produto(models.Model):
   c1_num = models.ForeignKey(Solicitacao, to_field='c1_num', default='', on_delete=models.DO_NOTHING)
   c1_item = models.CharField(max_length=4, null=False) 
   c1_produto = models.CharField(max_length=15, null=False) # b1_cod
   c1_descri = models.CharField(max_length=50, null=False) # b1_descri
   c1_um = models.CharField(max_length=2, null=False) # b1_um
   c1_filent = models.CharField(max_length=4, null=False, default='0101')
   c1_local = models.CharField(max_length=2, null=False) # b1_locpad
   b1_conta = models.CharField(max_length=20, null=False)
   c1_quant = models.DecimalField(max_digits=12, decimal_places=2)
   c1_cc = models.CharField(max_length=60, blank=True, null=True, default='')
   c1_datprf = models.DateField(blank=False, default='2025-01-01')
   ctj_desc = models.CharField(max_length=40, blank=True, default='')
   c1_obs = models.TextField(default="")
   r_e_c_n_o = models.BigIntegerField(primary_key=True, default=0)
   is_deleted = models.BooleanField(blank= False, default=False)  # Campo para controle de deleção

   def __str__(self):
      return self.c1_produto
   
   # def save(self, *args, **kwargs):
      
   #    connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"   
   #    with pyodbc.connect(connectionString) as conexao:
   #       with conexao.cursor() as cursor:
   #          cursor.execute("""SELECT MAX(R_E_C_N_O_)
   #                            FROM SC1010
   #                         """)
   #          recno = cursor.fetchone()
            
   #          self.r_e_c_n_o = recno + 1

   #    super().save(*args, **kwargs)

# class StatusPedido(models.Model):
#    recno = models.AutoField(db_column='R_E_C_N_O_', primary_key=True)  # Mapeia a coluna R_E_C_N_O_
#    C7_NUMSC = models.CharField(max_length=6)
#    C7_QUJE = models.FloatField()
#    C7_QTDACLA = models.FloatField()
#    C7_CONAPRO = models.CharField(max_length=1)
#    C7_TIPO = models.CharField(max_length=1)
#    C7_RESIDUO = models.CharField(max_length=1)
#    C7_QUANT = models.FloatField()
#    C7_CONTRA = models.CharField(max_length=1)

#    class Meta:
#       managed = False
#       db_table = 'SC7010'

#    objects = models.Manager().db_manager('protheus')

class StatusSC1(models.Model):
   recno = models.AutoField(db_column='R_E_C_N_O_', primary_key=True)
   C1_NUM = models.CharField(max_length=6)
   C1_COTACAO = models.CharField(max_length=6)
   C1_QUJE = models.FloatField()
   C1_APROV = models.CharField(max_length=1)
   C1_QUANT = models.DecimalField(max_digits=12, decimal_places=2, default=0)
   C1_RESIDUO = models.CharField(max_length=1, default='N')
   C1_IMPORT = models.CharField(max_length=1, default='N')
   C1_COMPRAC = models.CharField(max_length=1, default='2')
   C1_ITEM = models.CharField(max_length=4, null=False, default='0001' ) 
   C1_FILENT = models.CharField(max_length=4, null=False, default='0101')

   class Meta:
      managed: False
      db_table = 'SC1010'
   
   def get_status(self):
      status_mapping = [
         (self.C1_QUJE == 0 and self.C1_COTACAO in ['      ', 'IMPORT'] and self.C1_APROV == 'B', "Solicitação Bloqueada"),
         (self.C1_QUJE == 0 and self.C1_COTACAO == '      ' and self.C1_APROV == 'L', "Solicitação Pendente"),
         (self.C1_QUANT == self.C1_QUJE, "Solicitação Totalmente Atendida"),
         (self.C1_QUJE > 0 and self.C1_QUJE < self.C1_QUANT and self.C1_COTACAO == 'XXXXXX', "Solicitação Parcialmente Atendida Utilizada em Cotação"),
         (self.C1_QUJE > 0 and self.C1_QUJE < self.C1_QUANT, "Solicitação Parcialmente Atendida"),
         (self.C1_COTACAO != '      ', "Solicitação em Processo de Cotação"),
         (self.C1_RESIDUO == 'S', "Elim. por Resíduo"),
         (self.C1_IMPORT == 'S', "Solicitação de Produto Importado"),
         (self.C1_QUJE == 0 and self.C1_COTACAO in ['      ', 'IMPORT'] and self.C1_APROV == 'R', "Solicitação Rejeitada"),
         (self.C1_RESIDUO == 'S' and self.C1_COMPRAC == '1', "Solicitação em Compra Centralizada")
      ]

      for condition, tooltip in status_mapping:
        if condition:
            return tooltip

      return "Status Desconhecido"  



   def __str__(self):
      return self.get_status()

   objects = models.Manager().db_manager('protheus')


class RateioSC(models.Model):
   cx_filial = models.CharField(max_length=4, null=False, default='0101') # '0101'
   cx_solicit = models.ForeignKey(Solicitacao, to_field='c1_num', default='', on_delete=models.DO_NOTHING)
   cx_itemsol = models.CharField(max_length=4, null=False)
   cx_item = models.CharField(max_length=2, null=False)
   cx_perc = models.DecimalField(max_digits=6, decimal_places=2)
   cx_cc = models.CharField(max_length=9, null=False, default='')
   cx_conta = models.CharField(max_length=20, null=False, default='')
   cx_itemcta = models.CharField(max_length=9, null=False, default='')
   cx_clvl = models.CharField(max_length=9, null=False, default='')
   r_e_c_n_o = models.BigIntegerField(primary_key=True, default=0)

   def __str__(self):
      return self.c1_num