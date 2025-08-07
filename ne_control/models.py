from django.db import models
from django.conf import settings

# Por enquanto fazer com o nome da seção, porém verificar se vai ser isso ou o nome do militar, ou tlvz os dois.
# class Responsible(models.Model):
#     name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name

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
    # responsavel = models.ForeignKey(Responsible, on_delete=models.SET_NULL, null=True)
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    data_contato = models.CharField(max_length=10)

    def __str__(self):
        return self.cod_ne

    class Meta:
        verbose_name = "Note NE"
        verbose_name_plural = "Notes NE"

class ActionTaken(models.Model): # Medida tomada.
    cod_ne = models.ForeignKey(NoteNE, on_delete=models.CASCADE, related_name='actions_taken')
    date = models.DateField()
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    previ_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.description[:50] + '...'


# Tabela do Banco de Dados onde vão ser armazenadas as solicitações de reivindicação.
class Claim(models.Model):
    status = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cod_ne = models.ForeignKey(NoteNE, on_delete=models.CASCADE)


# class supplier(models.Model): # Fornecedor.
#     cod_ne = models.CharField(max_length=200)
#     # cod_fornecedor
#     # cnpj
#     # nome
#     # endereço? verificar se eh preciso o endereço


