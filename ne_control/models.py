from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, role='usuario', **extra_fields):
        if not username:
            raise ValueError("O nome de usuário é obrigatório")
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, role='admin', **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('visitor', 'Visitante'),
        ('other', 'Outro'),
    )

    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='visitor')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class note_ne(models.Model): # NE.
    cod_ne = models.CharField(max_length=50, primary_key=True)

    # cod_ne chave primaria
    # pi
    # nd
    # a liquidar
    # a pagar
    # total apagar
    # responsavel
    # cod fornecedor chave estrangeira


class action_taken(models.Model): # Medida tomada.
    cod_ne = models.CharField(max_length=200)
    # cod_ne chave estrangeira
    # data
    # responsavel chave estrangeira
    # previsão_data
    # descrição


class supplier(models.Model): # Fornecedor.
    cod_ne = models.CharField(max_length=200)
    # cod_fornecedor
    # cnpj
    # nome
    # endereço? verificar se eh preciso o endereço



