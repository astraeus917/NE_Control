from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'accounts/index.html')

@login_required
def register(request):
    return render(request, 'accounts/register.html')


def login_view(request):
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


def logout_view(request):
    logout(request)
    return redirect('login')







