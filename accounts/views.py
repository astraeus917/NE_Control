from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'accounts/index.html')


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





