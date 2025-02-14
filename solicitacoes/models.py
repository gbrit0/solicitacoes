from django.db import models
from django.contrib.auth import get_user_model 
from decimal import Decimal

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
      return self.c1_num
   
class Produto(models.Model):
   c1_num = models.ForeignKey(Solicitacao, to_field='c1_num', default='', on_delete=models.DO_NOTHING)
   c1_item = models.CharField(max_length=4, null=False) 
   c1_produto = models.CharField(max_length=15, null=False) # b1_cod
   c1_descri = models.CharField(max_length=50, null=False) # b1_descri
   c1_um = models.CharField(max_length=2, null=False) # b1_um
   c1_filent = models.CharField(max_length=4, null=False, default='0101')
   c1_local = models.CharField(max_length=2, null=False) # b1_locpad
   c1_quant = models.DecimalField(max_digits=12, decimal_places=2)
   c1_cc = models.CharField(max_length=60, null=False, default='')
   c1_datprf = models.DateField(blank=False, default='2025-01-01')
   ctj_desc = models.CharField(max_length=40, default='')
   c1_obs = models.CharField(max_length=30, default="")
   r_e_c_n_o = models.BigIntegerField(primary_key=True, default=0)
   usa_rateio = models.BooleanField(default=False)
    
   def total_percentual_rateio(self):
      if not self.usa_rateio:
         return Decimal('100.00')
      return sum(rateio.percentual for rateio in self.rateios.all())
   
   def save(self, *args, **kwargs):
      is_new = self.pk is None
      super().save(*args, **kwargs)
      
      # Se não usa rateio, não grava no banco
      if not self.usa_rateio and is_new:
         RateioProduto.objects.filter(produto=self).delete()
         

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

class StatusPedido(models.Model):
   recno = models.AutoField(db_column='R_E_C_N_O_', primary_key=True)  # Mapeia a coluna R_E_C_N_O_
   C7_NUMSC = models.CharField(max_length=6)
   C7_QUJE = models.FloatField()
   C7_QTDACLA = models.FloatField()
   C7_CONAPRO = models.CharField(max_length=1)
   C7_TIPO = models.CharField(max_length=1)
   C7_RESIDUO = models.CharField(max_length=1)
   C7_QUANT = models.FloatField()
   C7_CONTRA = models.CharField(max_length=1)

   class Meta:
      managed = False
      db_table = 'SC7010'

   objects = models.Manager().db_manager('protheus')

class StatusSC1(models.Model):
   recno = models.AutoField(db_column='R_E_C_N_O_', primary_key=True)
   C1_NUM = models.CharField(max_length=6)
   C1_COTACAO = models.CharField(max_length=6)
   C1_QUJE = models.FloatField()
   C1_APROV = models.CharField(max_length=1)

   class Meta:
      managed: False
      db_table = 'SC1010'

   objects = models.Manager().db_manager('protheus')



class ConfiguracaoRateio(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome

class ItemRateio(models.Model):
    configuracao = models.ForeignKey(ConfiguracaoRateio, on_delete=models.CASCADE, related_name='itens')
    centro_custo = models.CharField(max_length=60)
    percentual = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.centro_custo} - {self.percentual}%"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['configuracao', 'centro_custo'], name='unique_centro_custo_por_config')
        ]

class RateioProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='rateios')
    centro_custo = models.CharField(max_length=60)
    percentual = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.centro_custo} - {self.percentual}%"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['produto', 'centro_custo'], name='unique_centro_custo_por_produto')
        ]