from django.db import models
from datetime import datetime

from django.contrib.auth import get_user_model  # Correto

User = get_user_model()

class Solicitacao(models.Model):

   CHOICES_STATUS = [
      {"PENDENTE","Pendente"},
      {"APROVADO","Aprovado"},
      {"REJEITADO","Rejeitado"}
   ]

   CHOICES_TIPO = [
      {"COMPRAS", "Compras"},
      {"ARMAZEM", "Armazém"}
   ]

   solicitante = models.ForeignKey(User, on_delete=models.DO_NOTHING)
   tipo = models.CharField(max_length=100, choices=CHOICES_TIPO, default="COMPRAS", blank=False, null=False)
   produto = models.CharField(max_length=255, null=False, blank=False)
   quantidade = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
   data_de_necessidade = models.DateField(blank=False, null=False)
   obs = models.CharField(max_length=255, blank=False, null=False)
   data_cadastro = datetime.now()   
   status = models.CharField(max_length=100, choices=CHOICES_STATUS, default="")
