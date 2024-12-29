# forms.py
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model  # Correto
from usuarios.decorators import role_required

User = get_user_model()

class FiltroSolicitacaoForm(forms.Form):
    data_inicio = forms.DateField(
        required=False, 
        label='Data Início',
        widget=forms.DateInput(attrs={
            'type': 'date',  
            'class': 'row form-control gt-3',
            
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
        label='Usuário',
        widget=forms.Select(attrs={
            'class':'row form-select gt-3',
            'aria-label':"Todos",
            'placeholder':'Todos'
        })
    )

class SolicitacaoForm(forms.ModelForm):
    pass

class CadastrarSolicitacaoForm(forms.ModelForm):
    pass