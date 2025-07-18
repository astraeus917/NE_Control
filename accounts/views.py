from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from .forms import LoginForm

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
                form.add_error(None, "Usuário ou senha inválidos!")

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def register_user(request):
    return render(request, 'accounts/register.html')


def logout_user(request):
    logout(request)
    return redirect('login')

