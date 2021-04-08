from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import ReservaForm


def login(request):
    if request.method != 'POST':
        return render(request,'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    usuario_full = auth.authenticate(request, username=usuario, password=senha)

    if not usuario_full:
        messages.add_message(request, messages.ERROR, 'Usuário ou senha inválidos!')
        return redirect('login')
    else:
        auth.login(request,usuario_full)
        messages.add_message(request, messages.SUCCESS, 'Logado com sucesso!')
        return redirect('reserva')



def logout(request):
    auth.logout(request)
    return redirect('login')



def create(request):
    if request.method != 'POST':
        return render(request, 'accounts/create.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.add_message(request, messages.ERROR, 'Todos os campos são obrigatórios.')
        return render(request,'accounts/create.html')

    try:
        validate_email(email)
    except:
        messages.add_message(request, messages.ERROR, 'E-mail inválido.')
        return render(request,'accounts/create.html')

    if len(senha)< 6:
        messages.add_message(request, messages.ERROR, 'Senha muito curta. Mínimo de 6.')
        return render(request,'accounts/create.html')

    if senha != senha2: #validação de senha
        messages.add_message(request, messages.ERROR, 'Senhas não conferem.')
        return render(request, 'accounts/create.html')

    if len(usuario)< 6:
        messages.add_message(request, messages.ERROR, 'Usuário muito curto. Mínimo de 6.')
        return render(request,'accounts/create.html')

    if User.objects.filter(username= usuario).exists(): #verificção de user
        messages.add_message(request, messages.ERROR, 'Usuário já cadastrado.')
        return render(request, 'accounts/create.html')

    if User.objects.filter(email= email).exists(): #verificção de email
        messages.add_message(request, messages.ERROR, 'E-mail já cadastrado.')
        return render(request, 'accounts/create.html')

    messages.add_message(request, messages.SUCCESS, 'Usuário cadastrado com sucesso. Agora faça o login')
    user = User.objects.create_user(username=usuario, email= email, password= senha,
                                    first_name=nome, last_name= sobrenome)
    user.save()
    return redirect('login')



    
