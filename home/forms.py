# forms.py
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model  # Correto
from django.forms import formset_factory
from django.views.generic import CreateView
import pyodbc
import os

User = get_user_model()

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

class SolicitacaoForm(forms.ModelForm):
    pass

class CadastrarSolicitacaoForm(forms.ModelForm):
    pass