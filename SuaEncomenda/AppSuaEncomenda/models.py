from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Encomenda(models.Model):
    nome = models.CharField(max_length=200)
    #foto = models.ImageField(upload_to='img/bolos/')
    descricao = models.TextField(max_length=500)
    preco = models.DecimalField(max_digits=7 ,decimal_places=2)
    confeiteira = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome

    def get_absolute_url(self):
    	return reverse('AppSuaEncomenda:DetalheEncomenda', kwargs={'pk': self.pk})