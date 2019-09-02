from django.db import models

# Create your models here.

class Postagem(models.models):
	conteudo = models.TextField();
	data = models.DateTimeField();
	imagem = models.CharField();
	def __str__(self)
		return self.texto

class Comentario():
	autor = models.CharField();
	texto = models.CharField();
	def __str__(self)
		return self.texto	
