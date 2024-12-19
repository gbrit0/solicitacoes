# forms.py
from django import forms
from django.contrib.auth import get_user_model  # Correto

User = get_user_model()

from .models import Solicitacao

class FiltroSolicitacaoForm(forms.Form):
    data_inicio = forms.DateField(
        required=False, 
        label='Data Início',
        widget=forms.DateInput(attrs={
            'type': 'date',  # Importante para HTML5
            'class': 'row form-control gt-3',  # Para estilização
        })
    )
    data_fim = forms.DateField(
        required=False, 
        label='Data Fim',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'row form-control gt-3'
        })
    )
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        required=False, 
        label='Usuário'
    )


class SolicitacaoForms(forms.Form):
    tipo = forms.CharField(
        max_length=255,
        required=True,
        label='Tipo de Solicitação',
        widget=forms.DateInput(attrs={
            'class': 'row form-control gt-3'
        })
    )
    produto = forms.CharField(
        max_length=255,
        required=True,
        label='Produto',
        widget=forms.DateInput(attrs={
            'class': 'row form-control gt-3'
        })
    )
    quantidade = forms.FloatField(
        label="Quantidade",
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'row form-control gt-3'
        })
    )
    data_de_necessidade = forms.DateField(
        required=True,
        label="Data de Necessidade",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'row form-control gt-3'
        })
    )
    obs = forms.CharField(
        max_length=255,
        label="Observação (opcional)",
        widget=forms.DateInput(attrs={
            'class': 'row form-control gt-3'
        })
    )
    