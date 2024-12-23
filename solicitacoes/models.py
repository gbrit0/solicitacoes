from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model 
import pyodbc, os

User = get_user_model()

class Solicitacao(models.Model):
   c1_filial = '0101' # models.CharField(max_length=4, null=False) 
   c1_num = models.CharField(max_length=6, null=False, default='', primary_key=True) # max(sc1)
   c1_cc = models.CharField(max_length=60, null=False, default='')
   c1_datprf = models.DateField(blank=False)
   c1_solicit = "000000"
   c1_emissao = timezone.now
   c1_obs = models.CharField(max_length=30, null=False, default="")
   r_e_c_n_o = models.BigIntegerField()
   user = models.ForeignKey(User, to_field='cpf', default='', on_delete=models.DO_NOTHING)
   tipo = "compra"

   def __str__(self):
      return self.c1_num
   
   def save(self, *args, **kwargs):
      
      connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"   
      with pyodbc.connect(connectionString) as conexao:
         with conexao.cursor() as cursor:
            cursor.execute("""SELECT MAX(R_E_C_N_O_) + 1
                              FROM SC1010
                           """)
            recno = cursor.fetchall()
            # print(f"RECNOOOOOOOOOOOOOOOOOO    {recno[0][0]}")
            self.r_e_c_n_o = recno[0][0]

      super()  .save(*args, **kwargs)



class Produto(models.Model):
   c1_num = models.ForeignKey(Solicitacao, to_field='c1_num', default='', on_delete=models.DO_NOTHING)
   c1_item = models.CharField(max_length=4, null=False, primary_key=True) 
   c1_produto = models.CharField(max_length=15, null=False) # b1_cod
   c1_descri = models.CharField(max_length=50, null=False) # b1_descri
   c1_um = models.CharField(max_length=2, null=False) # b1_um
   c1_local = models.CharField(max_length=2, null=False) # b1_locpad
   c1_quant = models.DecimalField(max_digits=12, decimal_places=2)   

   def __str__(self):
      return self.c1_produto