from django.db import models

# Create your models here.
class Mensagens(models.Model):
	nome = models.CharField(max_length=100)
	texto = models.TextField(max_length=500)
	def __str__(self):
		return self.nome
