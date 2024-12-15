from django import forms
from utils.cpf_funcs import cpf_validate


class LoginForm(forms.Form):
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

class CadastroForm(forms.Form):
   primeiro_nome = forms.CharField(
      label="Nome",
      max_length=50,
      required=True,
      widget=forms.TextInput(
         attrs={
            "class": "form-control",
            "placeholder": "Ex. João"
         }
      )
   )
   sobrenome = forms.CharField(
      label="Sobrenome",
      max_length=50,
      required=True,
      widget=forms.TextInput(
         attrs={
            "class": "form-control",
            "placeholder": "Ex. Silva"
         }
      )
   )
   
   cpf = forms.CharField(
      label="CPF",
      max_length=11,
      validators=[cpf_validate],
      required=True,
      widget=forms.TextInput(
         attrs={
            "class": "form-control",
            "placeholder": "000.000.000-00"
         }
      )

   )

   senha1 = forms.CharField(
      label="Senha",
      max_length=50,
      required=True,
      widget=forms.PasswordInput(
         attrs={
            "class": "form-control",
            "placeholder": "Digite sua senha"
         }
      )
   )
   
   senha2 = forms.CharField(
      label="Confirmação",
      max_length=50,
      required=True,
      widget=forms.PasswordInput(
         attrs={
            "class": "form-control",
            "placeholder": "Confirma sua senha"
         }
      )
   )