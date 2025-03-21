from django import forms
from utils.cpf_funcs import cpf_validate
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.forms import ValidationError, inlineformset_factory
import pyodbc
import os
from datetime import date, timedelta


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
      fields = ['nome', 'email', 'cpf', 'role']
      
      widgets = {
         'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
         'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ex. joao@gmail.com'}),
         'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00', "onkeyup": "mascararCPF(this)"})
      }

   
   role = forms.ChoiceField(
      label="Papel",
      choices=CustomUser.ROLES,
      widget=forms.Select( attrs={'class': 'form-control', 'placeholder':'Papel'}),
      
   )

   # Adicione campos de senha explicitamente
   password1 = forms.CharField(
      label="Senha",
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Digite sua senha"})
   )
   
   password2 = forms.CharField(
      label="Confirme a Senha",
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirme sua senha"})
   )