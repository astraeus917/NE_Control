from django.shortcuts import render, redirect


def login_user(request):
    return render(request, 'accounts/login.html')


def register_user(request):
    return render(request, 'accounts/register.html')


def logout_user(request):
    return render(request, 'accounts/logout.html')

