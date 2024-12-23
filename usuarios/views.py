from django.shortcuts import render, redirect
from usuarios.forms import LoginForms, CadastroForms
from django.contrib import auth, messages
from django.contrib.auth import get_user_model  
from home.urls import lista_solicitacoes
import re, time
from django.contrib.auth.decorators import login_required

User = get_user_model()



def login(request):
   form = LoginForms()

   if request.method == 'POST':
      form = LoginForms(request.POST)

      if form.is_valid():
         cpf = form['cpf'].value()
         senha = form['senha'].value()

         cpf = re.sub(r'\D', '', cpf)

      usuario = auth.authenticate(
         request,
         username=cpf,
         password=senha
      )

      if usuario is not None:
         auth.login(request, usuario)
         messages.success(request, f"Login realizado com sucesso!")
         prox_pag = request.GET.get('next','lista_solicitacoes')
         return redirect(prox_pag)
      else:
         messages.error(request, f"É necessário logar para usar o sistema. Redirecionando...")
         time.sleep(3)
         return redirect('login')

   return render(request, 'usuarios/login.html', {"form": form})



@login_required(login_url='/login')
def cadastro(request):
    if request.method == 'POST':
        form = CadastroForms(request.POST)
        if form.is_valid():
            # Acesse os dados validados usando cleaned_data
            cpf = form.cleaned_data['cpf']
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            senha = form.cleaned_data['password1']

            # Verifique se o CPF já existe
            if User.objects.filter(cpf=cpf).exists():
               messages.error(request, "CPF já cadastrado.")
               return redirect('cadastro')

            # Crie o usuário
            usuario = User.objects.create_user(
               cpf=cpf,  # Use CPF como username
               email=email,
               password=senha,
               nome=nome  # Salve o nome no first_name
            )
            usuario.save()
            messages.success(request, "Usuário cadastrado com sucesso!",)
            return redirect('lista_solicitacoes')  

    else:
      form = CadastroForms()
      print("Erros de formulário:")
      for field, errors in form.errors.items():
            print(f"{field}: {errors}")
    
    return render(request, 'usuarios/cadastro.html', {"form": form})


def logout(request):
   auth.logout(request)
   return redirect('login')