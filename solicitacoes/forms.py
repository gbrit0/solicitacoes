from django import forms
import pyodbc
import os
from django.forms import inlineformset_factory
from solicitacoes.models import Produto, Solicitacao
from datetime import datetime, timedelta

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
        required=False,
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
            'class': 'form-control data-necessidade',
            'type':'date',
        }),
    )

    ctj_desc = forms.ChoiceField(
        required=False,
        label="Rateio",
        choices=[],
        widget=forms.Select(attrs={
            'class': 'selectsearch form-control',
            "data-live-search":"True",
            "data-size": '5',
            'Title': 'Sem Rateio',
        }),
    )

    c1_obs = forms.CharField(
        required=True,
        label="Observação",
        widget=forms.Textarea(attrs={
            'class':'form-control',
            'placeholder':'Digite sua observação aqui...',
            'rows':2
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
    
    b1_conta = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    
    c1_filent = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    b1_locpad = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if not self.instance.pk:
        self.fields['c1_datprf'].initial = datetime.now().date() + timedelta(days=15) # inicializa com data de necessidade 15 dias adiante

        connectionString = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.environ['HOST']};DATABASE={os.environ['DATABASE']};UID={os.environ['USER']};PWD={os.environ['PASSWORD']};TrustServerCertificate=yes"
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
                                -- AND CTT_FILIAL = '0101'
                                AND CTT_CLASSE = '2'""")
                
                # <=========== DESCOMENTAR O CTT_FILIAL QUANDO COLOCAR EM PRODUÇÃO ==================>

                centros_de_custo = cursor.fetchall()
                self.fields['c1_cc'].choices = centros_de_custo

                cursor.execute("""SELECT DISTINCT 
                                    CTJ_RATEIO, 
                                    CTJ_DESC 
                                FROM CTJ010 
                                WHERE D_E_L_E_T_ <> '*' 
                                    AND CTJ_FILIAL = '0101'""")
                
                rateios = cursor.fetchall()
                self.fields['ctj_desc'].choices = rateios


    def clean(self):
        cleaned_data = super().clean()
        cc = cleaned_data.get('c1_cc')
        rateio = cleaned_data.get('ctj_desc')
        
        if not cc and not rateio:
            # Adiciona o erro aos campos específicos

            self.add_error('c1_cc', 'Preencha Centro de Custo ou Rateio')
            self.add_error('ctj_desc', 'Preencha Centro de Custo ou Rateio')
            
            raise forms.ValidationError("Você deve preencher pelo menos um dos campos: Centro de Custo ou Rateio")
            
        return cleaned_data

ProductFormset = inlineformset_factory(
      Solicitacao,
      Produto,
      form=ProdutosForm,
      fields=('c1_cc', 'c1_produto', 'c1_datprf', 'c1_quant', 'c1_obs', 'ctj_desc'),
      extra=1,
      can_delete=True,
      can_delete_extra=True
   )