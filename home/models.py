from django.db import models
from datetime import datetime
from django.utils import timezone
import pyodbc
import os
from django.contrib.auth import get_user_model  # Correto

User = get_user_model()

class Solicitacao(models.Model):
   class Meta:
      managed = False
   c1_filial = '0101' # models.CharField(max_length=4, null=False)
   c1_num = models.CharField(max_length=6, null=False) # max(sc1)
   c1_cc = models.CharField(max_length=60, null=False, default='')
   c1_item = models.CharField(max_length=4, null=False)
   c1_produto = models.CharField(max_length=60, null=False) # Acessar o nome do produto a partir do codigo self.c1_produto.b1_desc
   c1_descri = models.CharField(max_length=50, null=False, default="")
   c1_local = models.CharField(max_length=2, null=False)
   c1_quant = models.DecimalField(max_digits=12, decimal_places=2)
   c1_datprf = models.DateField()
   c1_user = "000000"
   c1_emissao = timezone.now
   r_e_c_n_o = models.BigIntegerField()

   def save(self, *args, **kwargs):
      
      connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"   
      with pyodbc.connect(connectionString) as conexao:
         with conexao.cursor() as cursor:
            cursor.execute("""SELECT MAX(R_E_C_N_O_) + 1
                              FROM SC1010
                           """)
            self.r_e_c_n_o = cursor.fetchall()

      if self.c1_produto:
         self.c1_descri = self.c1_produto.b1_desc
         self.c1_local = self.c1_produto.b1_locpad
      
      
      super.save(*args, **kwargs)
   
