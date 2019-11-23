from django.db import models


class Encomenda(models.Model):
    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=45)
    descricao = models.TextField(max_length=500)
    preco = models.DecimalField(max_digits=7 ,decimal_places=2)
    def __str__(self):
        return self.nome