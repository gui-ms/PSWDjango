from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        # Validations:

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem!')
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha precisa ter mais de 6 caracteres!')
            return redirect('/usuarios/cadastro')

        users = User.objects.filter(username=username)
        
        if users.exists():
            messages.add_message(request, constants.ERROR, 'Usuário já cadastrado!')
            return redirect('/usuarios/cadastro')
        
        user = User.objects.create_user(username=username, password=senha)
        return redirect('/usuarios/logar')

def logar(request):
    return render(request, 'logar.html')