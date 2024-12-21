from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model 

User = get_user_model()

class Solicitacao(models.Model):
   c1_filial = '0101' # models.CharField(max_length=4, null=False) 
   c1_num = models.CharField(max_length=6, null=False, default='', primary_key=True) # max(sc1)
   c1_cc = models.CharField(max_length=60, null=False, default='')
   c1_datprf = models.DateField()
   c1_user = "000000"
   c1_emissao = timezone.now
   r_e_c_n_o = models.BigIntegerField()
   user = models.ForeignKey(User, to_field='cpf', default='', on_delete=models.DO_NOTHING)

   def __str__(self):
      return self.c1_num

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