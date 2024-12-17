from django import forms
from utils.cpf_funcs import cpf_validate
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


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
        model = CustomUser  # Ou seu CustomUser, se tiver um
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




# class CadastroForms(UserCreationForm):
#    class Meta:
#       model = CustomUser
#       fields = ['cpf', 'email', 'nome'] # , 'Senha'

#       widgets = {
#          'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
#          'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ex. joao@gmail.com'}),
#          'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00', "onkeyup": "mascararCPF(this)"}),
         # 'Senha': forms.PasswordInput(attrs={"class": "form-control","placeholder": "Digite sua senha"}),
         
      # }

   # nome = forms.CharField(
   #    label="Nome",
   #    max_length=255,
   #    required=True,
   #    widget=forms.TextInput(
   #       attrs={
   #          "class": "form-control",
   #          "placeholder": "Ex. João"
   #       }
   #    )
   # )
   # email = forms.EmailField(
   #    label="Email",
   #    max_length=80,
   #    required=True,
   #    widget=forms.EmailInput(
   #       attrs={
   #          "class": "form-control",
   #          "placeholder": "Ex. joao@gmail.com"
   #       }
   #    )
   # )
   # cpf = forms.CharField(
   #    label="CPF",
   #    max_length=14,
   #    validators=[cpf_validate],
   #    required=True,
   #    widget=forms.TextInput(
   #       attrs={
   #          "class": "form-control",
   #          "placeholder": "000.000.000-00",
   #          "onkeyup": "mascararCPF(this)"
   #       }
   #    )

   # )

   # senha1 = forms.CharField(
   #    label="Senha",
   #    max_length=50,
   #    required=True,
   #    widget=forms.PasswordInput(
   #       attrs={
   #          "class": "form-control",
   #          "placeholder": "Digite sua senha"
   #       }
   #    )
   # )
   
   # senha2 = forms.CharField(
   #    label="Confirmação da senha",
   #    max_length=50,
   #    required=True,
   #    widget=forms.PasswordInput(
   #       attrs={
   #          "class": "form-control",
   #          "placeholder": "Confirma sua senha"
   #       }
   #    )
   # )