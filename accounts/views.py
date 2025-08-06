from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterForm

# Seta o modelo do Usuario, modelo personalizado criado no models.
User = get_user_model()

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('list')
            
            else:
                messages.error(request, "Usuário ou senha inválidos!")

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, "As senhas não coincidem!")
            else:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Este nome de usuário já existe!")
                else:
                    user = User.objects.create_user(username=username, password=password)
                    return redirect('login')
    
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')

