from django.db import models
from usuario.models import Perfil
from livro.models import Livro

class LivroUsuario(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT)
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT)
    estado_choices = [
        (0, 'Excelente'),
        (1, 'Ótimo'),
        (2, 'Bom'),
        (3, 'Regular'),
        (4, 'Ruim'),
        (5, 'Péssimo'),
    ]
    estado = models.IntegerField(choices = estado_choices, default = 0) 

class TrocaLivro(models.Model):
    livro_solicitante  = models.ForeignKey(LivroUsuario, on_delete = models.CASCADE, related_name = "livro_solicitante", null=True)
    livro_solicitado = models.ForeignKey(LivroUsuario, on_delete = models.CASCADE, related_name = "livro_solicitado", null=True)
    confirmacao = models.BooleanField(null = True)
    data_solicitacao  = models.DateTimeField(auto_now_add = True)
    data_finalizacao  = models.DateTimeField(blank=True, null=True)