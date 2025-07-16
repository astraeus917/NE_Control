from django.shortcuts import render


def index(request):
    return render(request, 'accounts/index.html')


def register(request):
    return render(request, 'accounts/register.html')


