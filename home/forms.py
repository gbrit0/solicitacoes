# forms.py
from django import forms

class FiltroSolicitacaoForm(forms.Form):
    data_inicio = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={
            'type': 'date',  # Importante para HTML5
            'class': 'form-control'  # Para estilização
        })
    )
    data_fim = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )