from django import forms
from utils.cpf_funcs import cpf_validate
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.forms import ValidationError
import mysql.connector
import os

class LoginForms(forms.Form):
   cpf = forms.CharField(
      label="CPF",
      max_length=14,
      validators=[cpf_validate],
      required=True,
      widget=forms.TextInput(
         attrs={
            "class": "form-control",
            "placeholder": "000.000.000-00",
            "onkeyup": "mascararCPF(this)"
         }
      )

   )

   senha = forms.CharField(
      label="Senha",
      max_length=50,
      min_length=8,
      required=True,
      widget=forms.PasswordInput(
         attrs={
            "class": "form-control",
            "placeholder": "Digite sua senha"
         }
      )
   )

class CadastroForms(UserCreationForm):
   class Meta:
      model = CustomUser
      fields = ['nome', 'email', 'cpf']
      
      widgets = {
         'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
         'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ex. joao@gmail.com'}),
         'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00', "onkeyup": "mascararCPF(this)"}),
      }

   # Adicione campos de senha explicitamente
   password1 = forms.CharField(
      label="Senha",
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Digite sua senha"})
   )
   
   password2 = forms.CharField(
      label="Confirme a Senha",
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirme sua senha"})
   )


class SolicitacaoForms(UserCreationForm):
   c1_filial = forms.CharField(
      label="Filial do Sistema",
      max_length=4,
      required=False,
      default="0101        ",
      choices=[],
      widget=forms.PasswordInput(
         attrs={
            "class": "form-control",
            "placeholder": "Digite sua senha novamente"
         }
      )
   )
   # c1_num                # O app deve buscar no campo e preencher automaticamente

   # c1_item               # O app deve criar automaticamente numeros sequenciais 4 dígitos

   b1_desc = forms.ChoiceField(
      label="Produto",
      required=True,
      choices=[],
      widget=forms.PasswordInput(
         attrs={
            "class": "form-control",
            "placeholder": "Digite sua senha novamente"
         }
      ),
      default=""
   )





   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      pool = mysql.connector.pooling.MySQLConnectionPool(
         pool_name="MySqlPool",
         pool_size=10,
         user=os.environ['USER'],
         password=os.environ['PASSWORD'],
         host=os.environ['HOST'],
         database=os.environ['DATABASE']
      )
      with pool.get_connection() as conexaoComBanco:
         with conexaoComBanco.cursor() as cursor:

            cursor.execute("""SELECT 
                                 M0_CODFIL AS cod_filial, 
                                 M0_FILIAL AS filial 
                              FROM SYS_COMPANY 
                              WHERE D_E_L_E_T_ = '' 
                              AND M0_NOME = 'BRG Geradores';""")
            filiais = cursor.fetchall()

            cursor.execute("""SELECT TOP 100
                                 B1_COD AS cod_produto,
                                 B1_DESC AS produto
                              FROM SB1010
                              WHERE B1_FILIAL = '01'""")
            produtos = cursor.fetchall()

      self.fields['c1_filial'].choices = filiais
      self.fields['b1_desc'].choices = produtos