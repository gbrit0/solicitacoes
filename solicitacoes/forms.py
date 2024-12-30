from django import forms
import pyodbc
import os
from django.forms import inlineformset_factory
from solicitacoes.models import Produto, Solicitacao

class SolicitacaoForm(forms.ModelForm):
    class Meta:
        model = Solicitacao
        fields = ['c1_filial', 'c1_num', 'c1_solicit', 'c1_emissao', 'user', 'tipo']

    widgets={
        'c1_filial':forms.HiddenInput(),
        'c1_num':forms.HiddenInput(),
        'c1_solicit':forms.HiddenInput(),
        'c1_emissao':forms.HiddenInput(),
        'user':forms.HiddenInput(),
        'tipo':forms.HiddenInput(),
    }
    

class ProdutosForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['c1_produto', 'c1_quant', 'c1_cc', 'c1_datprf', 'c1_obs']


    c1_produto = forms.ChoiceField(
        required=True,
        label="Produto",
        choices=[],
        widget=forms.Select(attrs={
            'class': 'selectsearch form-control',
            "data-live-search":"True",
            "data-size": '5',
            'title':'Selecione um produto'
        }),
    )

    c1_quant = forms.DecimalField(
        required=True,
        label='Quantidade',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Quantidade',
        }),
    )
    
    c1_cc = forms.ChoiceField(
        required=True,
        label="Centro de Custo",
        choices=[],
        widget=forms.Select(attrs={
            'class': 'selectsearch form-control',
            "data-live-search":"True",
            "data-size": '5',
            'Title': 'Selecione um centro de custo',
        }),
    )
    c1_datprf = forms.DateField(
        required=True,
        label="Data de Necessidade",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type':'date',
            'placeholder': 'Data de Necessidade',
        }),
    )

    c1_obs = forms.CharField(
        required=True,
        label="Observação",
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Observação'
        })
    )
    
    b1_cod = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    b1_um = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    b1_locpad = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    DELETE = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"
        with pyodbc.connect(connectionString) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("""SELECT 
                                     TRIM(B1_COD) AS cod_produto,
                                     TRIM(B1_DESC) as produto
                                  FROM SB1010
                                  WHERE D_E_L_E_T_ <> '*'
                                  AND B1_MSBLQL = '2'
                                  AND B1_FILIAL = '01'""")
                
                produtos = cursor.fetchall()
                self.fields['c1_produto'].choices = [(p[0], p[1]) for p in produtos]
                
                cursor.execute("""SELECT 
                                    CTT_CUSTO, 
                                    CTT_DESC01 
                                FROM CTT010 
                                WHERE D_E_L_E_T_ <> '*'
                                AND CTT_BLOQ = '2'
                                AND CTT_FILIAL = '0101'
                                AND CTT_CLASSE = '2'""")
                
                centros_de_custo = cursor.fetchall()
                self.fields['c1_cc'].choices = centros_de_custo


ProductFormset = inlineformset_factory(
      Solicitacao,
      Produto,
      form=ProdutosForm,
      fields=('c1_cc', 'c1_produto', 'c1_datprf', 'c1_quant', 'c1_obs'),
      extra=1,
      can_delete=True,
      can_delete_extra=True
   )
