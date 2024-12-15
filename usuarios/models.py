from django.db import models
from datetime import datetime
from utils.cpf_funcs import cpf_validate


class User(models.Model):
   cpf = models.CharField(
      primary_key=True,
      max_length=11,
      blank=False,
      null=False,
      validators=[cpf_validate]
   )
   nome = models.CharField(max_length=50, null=False, blank=False)
   sobrenome = models.CharField(max_length=100, null=False, blank=False)
   email = models.EmailField(max_length= 255,  blank=False)
   data_cadastro = datetime.now()
   admin = models.BooleanField(default=False)

   def __str__(self):
      return f"{self.nome} {self.sobrenome}"

   def clean_cpf(self):
      return "".join(char for char in self.cpf if char.isdigit())
   
