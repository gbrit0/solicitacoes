from django import forms
import pyodbc
import os
from solicitacoes.models import Produto, Solicitacao

class SolicitacaoForm(forms.ModelForm):
    class Meta:
        model = Solicitacao
        fields = ['c1_cc', 'c1_datprf']

    c1_cc = forms.ChoiceField(
        required=True,
        label="Centro de Custo",
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Centro de Custo',
        }),
    )
    c1_datprf = forms.DateField(
        required=True,
        label="Data de Necessidade",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Data de Necessidade',
        }),
    )
        
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"   
        
        with pyodbc.connect(connectionString) as conexao:
            with conexao.cursor() as cursor:
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

class ProdutosForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['c1_descri', 'c1_quant']


    c1_descri = forms.ChoiceField(
        required=True,
        label="Produto",
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Produto',
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"
        with pyodbc.connect(connectionString) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("""SELECT 
                                     TRIM(B1_COD) + TRIM(B1_UM) + TRIM(B1_LOCPAD) AS cod_produto,
                                     B1_DESC as produto
                                  FROM SB1010
                                  WHERE D_E_L_E_T_ <> '*'
                                  AND B1_MSBLQL = '2'
                                  AND B1_FILIAL = '01'""")
                
                produtos = cursor.fetchall()
                self.fields['c1_descri'].choices = [(p[0], p[1]) for p in produtos]