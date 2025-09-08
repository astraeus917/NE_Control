from django import forms
from .models import Workplace

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 bg-gray-150 rounded-md',
            'placeholder': 'Digite seu nome de usuário'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 bg-gray-150 rounded-md',
            'placeholder': 'Digite sua senha de acesso'
        })
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 bg-gray-150 rounded-md',
            'placeholder': 'Digite seu nome de usuário'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 bg-gray-150 rounded-md',
            'placeholder': 'Digite sua senha de acesso'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 bg-gray-150 rounded-md',
            'placeholder': 'Confirme sua senha de acesso'
        })
    )
    workplace = forms.ModelChoiceField(
        queryset=Workplace.objects.all(),
        required=False,
        empty_label="Selecione sua seção",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 bg-gray-150 rounded-md text-gray-100'
        })
    )

class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-xl px-4 py-2 bg-gray-150 rounded-md',
            'placeholder': 'Digite sua senha de acesso'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-xl px-4 py-2 bg-gray-150 rounded-md',
            'placeholder': 'Confirme sua senha de acesso'
        })
    )    

