from django.db import models
from django.utils import timezone
import datetime
from django.utils import timezone
#import biblioteca.models as bibmodels

from biblioteca.models import *


class Livro(models.Model):
    nome = models.CharField(max_length=100)
    isbn_10 = models.CharField(max_length=10)
    isbn_13 = models.CharField(max_length=13)
    editora = models.CharField(max_length=50)
    capa = models.ImageField(upload_to='images/livros/')
    genero_choices = [
        (0, 'Ação'),
        (1, 'Administração'),
        (2, 'Aventura'), 
        (3, 'Arte'),
        (4, 'Artesanato'),
        (5, 'Autoajuda'),
        (6, 'Biografia'),
        (7, 'Ciência'),
        (8, 'Computação'),
        (9, 'Humor'),
        (10, 'Direito'),
        (11, 'Educação'),
        (12, 'Didático'),
        (13, 'Engenharia'),
        (14, 'Erótico'),
        (15, 'Esporte'),
        (16, 'Ficção'),
        (17, 'Gastronomia'),
        (18, 'História'),
        (19, 'Quadrinho'),
        (20, 'Infantil'),
        (21, 'Infantojuvenil'),
        (22, 'LGBTQI+'),
        (23, 'Literatura'),
        (24, 'Medicina'),
        (25, 'Policial'),
        (26, 'Religião'),
        (27, 'Romance'),
        (28, 'Saúde'),
        (29, 'Turismo'),
        (30, 'Linguagem')
    ]
    genero = models.IntegerField(choices=genero_choices, default=0)
    status = models.BooleanField(default=True)
    autor = models.TextField()
    resumo = models.TextField()
    

    last_reseted_views = models.DateField(default = datetime.date(2000, 1, 1))
    visualizacoes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nome
    def GeneroNome(self):
        return self.genero_choices[self.genero][1]
    def Autores(self):
        autores = self.autor.split(";")
        ret = []
        for i in autores:
            ret.append(i.strip())
        return ret
    def Serializer(self):
        from biblioteca.models import LivroAssociado
        
        livros = LivroAssociado.objects.filter(livro = self)
        print(livros)
        ret = {
            "nome":self.nome,
            "capa": self.capa.url,
            "autores": self.Autores(),
            "genero": self.GeneroNome(),
            "disponivel": livros,
            "id": self.id
        }
        return ret
