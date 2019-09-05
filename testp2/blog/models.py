from django.db import models

# Create your models here.

class Postagem(models.Model):
	conteudo = models.TextField(max_length = 200);
	data = models.DateTimeField('Data de publicação');
	imagem = models.CharField(max_length = 200);
	def __str__(self):
		return self.conteudo

class Comentario(models.Model):
	autor = models.CharField(max_length = 200);
	texto = models.CharField(max_length = 200);
	postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE, null=True)
	def __str__(self):
		return self.texto	
