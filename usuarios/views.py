from django.shortcuts import render, redirect
from usuarios.forms import LoginForms, CadastroForms
from django.contrib import auth, messages
from django.contrib.auth import get_user_model  # Correto

User = get_user_model()



def login(request):
   form = LoginForms()

   if request.method == 'POST':
      form = LoginForms(request.POST)

      if form.is_valid():
         cpf = form['cpf'].value()
         senha = form['senha'].value()

      usuario = auth.authenticate(
         request,
         username=cpf,
         password=senha
      )

      if usuario is not None:
         auth.login(request, usuario)
         messages.success(request, f"Login realizado com sucesso!")
         return redirect('home')
      else:
         messages.error(request, f"Erro ao efetuar login. Tente novamente.")
         return redirect('login')

   return render(request, 'usuarios/login.html', {"form": form})

# def cadastro(request):
#    form = CadastroForms()

#    if request.method == 'POST':
#       form = CadastroForms(request.POST)

#       if form.is_valid():
#          nome = form['nome'].value()
#          email = form['email'].value()
#          cpf = form['cpf'].value()
#          senha = form['senha'].value()

#       if User.objects.filter(cpf=cpf).exists():
#          messages.error(request, f"Cpf já cadastrado.")
#          return redirect('cadastro')
      
#       usuario = User.objects.create_user(
#          username=nome,
#          cpf=cpf,
#          email=email,
#          password=senha
#       )
#       usuario.save()
#       messages.success(request, f"Usuário cadastrado com sucesso!")
#       return redirect('usuarios/cadastro.html')

#    return render(request, 'usuarios/cadastro.html', {"form": form})

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForms(request.POST)
        if form.is_valid():
            # Acesse os dados validados usando cleaned_data
            cpf = form.cleaned_data['CPF']
            nome = form.cleaned_data['Nome']
            email = form.cleaned_data['Email']
            senha = form.cleaned_data['password1']  # Password fields são password1 e password2

            # Verifique se o CPF já existe
            if User.objects.filter(username=cpf).exists():
                messages.error(request, "CPF já cadastrado.")
                return redirect('cadastro')

            # Crie o usuário
            usuario = User.objects.create_user(
                username=cpf,  # Use CPF como username
                email=email,
                password=senha,
                first_name=nome  # Salve o nome no first_name
            )
            usuario.save()
            messages.success(request, "Usuário cadastrado com sucesso!")
            return redirect('login')  # Redirecione para a página de login ou outra página desejada

    else:
        form = CadastroForms()
    
    return render(request, 'usuarios/cadastro.html', {"form": form})
