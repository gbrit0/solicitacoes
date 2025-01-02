from django.shortcuts import render, redirect
from usuarios.forms import LoginForms, CadastroForms
from django.contrib import auth, messages
from django.contrib.auth import get_user_model  
from .decorators import role_required
import re, time
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

User = get_user_model()

# Teste dpara validação do encaminhamento da requisição pelo Augusto
# def teste(request):
#     print(f"Entrou em 'teste'")
#     return render(request, 'usuarios/teste.html')

def login(request):
    form = LoginForms()
    
    # Mover a verificação de timeout_message para depois da criação do form
    if request.session.get('timeout_message'):
        messages.error(request, "Você foi desconectado devido ao limite de tempo de sessão.")
        del request.session['timeout_message']
    
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
                messages.success(request, "Login realizado com sucesso!")
                prox_pag = request.GET.get('next','lista_solicitacoes')
                return redirect(prox_pag)
            else:
                messages.error(request, "Erro no login!")
                return redirect('login')

    return render(request, 'usuarios/login.html', {"form": form})


@role_required(['admin',])
@login_required(login_url='login')
def cadastro(request):
    
    if request.method == 'POST':
        form = CadastroForms(request.POST)
        if form.is_valid():
            try:
                # Acesse os dados validados usando cleaned_data
                # cpf = form.cleaned_data['cpf']
                cpf = str(re.sub(r'\D', '', form.cleaned_data['cpf']))
                nome = form.cleaned_data['nome']
                email = form.cleaned_data['email']
                senha = form.cleaned_data['password1']
                role = form.cleaned_data['role']
                id = str(int(User.objects.latest('id').id) + 1).zfill(6)
                
                # Verifique se o CPF já existe
                if User.objects.filter(cpf=cpf).exists():
                    messages.error(request, "CPF já cadastrado.")
                    return render(request, 'usuarios/cadastro.html', {"form": form})

                try:
                    User.objects.create_user(
                        cpf=cpf,
                        email=email,
                        password=senha,
                        nome=nome,
                        role=role,
                        id=id
                    )
                except IntegrityError:
                    messages.error(request, "Erro: Este CPF já está cadastrado no sistema.")
                    return render(request, 'usuarios/cadastro.html', {"form": form})
                messages.success(request, "Usuário cadastrado com sucesso!")
                return redirect('lista_solicitacoes')

            except Exception as e:
                messages.error(request, f"Erro ao cadastrar usuário: {str(e)}")
                return render(request, 'usuarios/cadastro.html', {"form": form})
    else:
        form = CadastroForms()

    return render(request, 'usuarios/cadastro.html', {"form": form})


def logout(request):
   auth.logout(request)
   messages.success(request, f"Você será redirecionado para a página de login!")
   time.sleep(3)
   return redirect('login')

