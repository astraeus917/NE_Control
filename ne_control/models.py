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


# Por enquanto fazer com o nome da seção, porém verificar se vai ser isso ou o nome do militar, ou tlvz os dois.
class Responsible(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Unica tabela com campos em portugues por conta do esquema csv.
class NoteNE(models.Model): # NE.
    cod_ne = models.CharField(max_length=50, primary_key=True)
    ug = models.BigIntegerField()
    pi = models.CharField(max_length=200)
    nd = models.BigIntegerField()
    dias = models.IntegerField()
    a_liquidar = models.DecimalField(max_digits=10, decimal_places=2)
    liquidado_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    total_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    pago = models.DecimalField(max_digits=10, decimal_places=2)
    responsavel = models.ForeignKey(Responsible, on_delete=models.SET_NULL, null=True)
    data_contato = models.CharField(max_length=10)

    def __str__(self):
        return self.cod_ne

    class Meta:
        verbose_name = "Note NE"
        verbose_name_plural = "Notes NE"


# class action_taken(models.Model): # Medida tomada.
#     cod_ne = models.CharField(max_length=200)
#     # cod_ne chave estrangeira
#     # data
#     # responsavel chave estrangeira
#     # previsão_data
#     # descrição


# class supplier(models.Model): # Fornecedor.
#     cod_ne = models.CharField(max_length=200)
#     # cod_fornecedor
#     # cnpj
#     # nome
#     # endereço? verificar se eh preciso o endereço



