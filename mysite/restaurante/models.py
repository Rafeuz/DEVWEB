from django.db import models

# Create your models here.
class Produto(models.Model):
	nome = models.CharField(max_length = 45)
	preco = models.DecimalField(max_digits = 7, decimal_places = 2)
	disponibilidade = models.BooleanField()
	def __str__(self):
		return self.nome

class Comanda(models.Model):
	mesa = models.IntegerField()
	esta_ativa = models.BooleanField()
	itens = models.ForeignKey('ItemComanda', on_delete = models.CASCADE)

class ItemComanda(models.Model):
	qtd = models.IntegerField()
	produto = models.ForeignKey('Produto', on_delete = models.CASCADE)