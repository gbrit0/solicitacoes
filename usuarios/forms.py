from django import forms
from utils.cpf_funcs import cpf_validate
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.forms import ValidationError, inlineformset_factory
import pyodbc
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

class ProdutoForm(forms.Form):
   b1_desc = forms.ChoiceField(           # setar este valor no campo c1_produto da SC1010
      label="Produto",
      required=True,
      choices=[],
      widget=forms.Select(
         attrs={
            "class": "form-control selectpicker",
            "data-live-search":"true",
            "placeholder": "Produto"
         }
      )
   )
   c1_local = forms.ChoiceField(
      label="Armazém",
      required=True,
      choices=[], 
      widget=forms.Select(
         attrs={
            "class": "form-control selectpicker",
            "data-live-search":"true",
            "placeholder": "Armazém"
         }
      )
   )
   c1_quant = forms.FloatField(
      label = "Quantidade",
      required=True,
      widget=forms.NumberInput(
         attrs={
            "class":"form-control",
            "placeholder":"Quantidade"
         }
      )
   )
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"
      
      
      with pyodbc.connect(connectionString) as conexao:
         with conexao.cursor() as cursor:
            cursor.execute("""SELECT 
                                 TRIM(' ' FROM B1_LOCPAD) + TRIM(' ' FROM B1_UM) + TRIM(' ' FROM B1_COD) AS cod_produto,
                                 B1_DESC AS produto
                              FROM SB1010
                              WHERE D_E_L_E_T_ <> '*'
                              AND B1_MSBLQL = '2'
                              AND B1_FILIAL = '01'
                           """)
            produtos = cursor.fetchall()

      self.fields['b1_desc'].choices = produtos


class SolicitacaoForms(forms.Form):
   
   c1_filial = forms.ChoiceField(         # a princípio preencher '0101' BRG Matriz mas futuramente liberar para user escolher a filial
      label="Filial do Sistema",
      required=False,
      choices=[],
      widget=forms.Select(
         attrs={
            "class": "form-control selectpicker",
            "data-live-search":"true",
            "placeholder": "Filial do Sistema"
         }
      )
   )
   # c1_num
   # c1_item

   c1_cc = forms.ChoiceField(         # setar este valor no campo C1_CC da SC1010
      label="Centro de Custo",
      required=True,
      choices=[],
      widget=forms.Select(
         attrs={
            "class": "form-control selectpicker",
            "data-live-search":"true",
            "placeholder": "Filial do Sistema"
         }
      )
   )

   c1_datprf = forms.DateField(
      label="Data de Necessidade",
      required=True,
      widget=forms.DateInput(
         attrs={
            "class": "form-control",
            "type": "date"
         }
      )
   ) 

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"
      
      
      with pyodbc.connect(connectionString) as conexao:
         with conexao.cursor() as cursor:

            cursor.execute("""SELECT 
                                 M0_CODFIL AS cod_filial, 
                                 M0_FILIAL AS filial 
                              FROM SYS_COMPANY 
                              WHERE D_E_L_E_T_ = '' 
                              AND M0_NOME = 'BRG Geradores';""")
            filiais = cursor.fetchall()


            cursor.execute(f"""SELECT
                                 -- CTT_FILIAL,
                                 CTT_CUSTO AS cod_centro_de_custo, 
                                 CTT_DESC01 AS centro_de_custo
                              FROM CTT010
                              WHERE D_E_L_E_T_ <> '*' 
                              AND CTT_BLOQ = '2' 
                              AND CTT_CLASSE = '2'
                              AND CTT_FILIAL = '0101'""")
            centros_de_custo = cursor.fetchall()
            cursor.execute("SELECT DISTINCT CTT_FILIAL FROM CTT010")
            # for cc in centros_de_custo:
            #    print(cc)

      self.fields['c1_filial'].choices = filiais
      self.fields['c1_cc'].choices = centros_de_custo