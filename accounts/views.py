from django.contrib.auth import authenticate, login, logout as site_logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm


def index(request):
    return render(request, 'accounts/index.html')

@login_required
def register(request):
    return render(request, 'accounts/register.html')


def access_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return render(request, 'index.html', {'error': 'Usuário ou senha inválidos'})

    return render(request, 'index.html')


def register_user(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'accounts/register.html', {'form': form})


def logout(request):
    site_logout(request)
    return redirect('login')







