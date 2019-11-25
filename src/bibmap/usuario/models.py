import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from biblioteca.models import Endereco, Biblioteca
from django.contrib.auth.models import Group, Permission
from livro.models import Livro
import random
# Create your models here.

class Telefone(models.Model):
    numero = models.CharField(max_length = 14) #(XX)XXXXX-XXXX

    def __str__(self):
        return self.numero

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete = models.CASCADE, null = True)
    telefone = models.ForeignKey(Telefone, on_delete = models.CASCADE, null = True)
    sexo_choices = [
        (1, 'Feminino'),
        (2, 'Masculino'),
    ]
    
    grupos_possiveis = [
        (0, "Usuário"),
        (1, "Operador"),
        (2, "Administrador"),
    ]
    sexo = models.IntegerField(choices = sexo_choices)
    foto = models.ImageField(upload_to = 'images/user/')
    data_de_registro = models.DateTimeField(auto_now_add = True)
    grupo = models.IntegerField(default=0, choices=grupos_possiveis)

    def GetFavGeneros(self):
        generos = self.generolivro_set.all()
        return generos;

    def GetGeneroFavorito(self):
        genero = GeneroLivro.objects.filter(perfil=self)[0]
        return genero;
    
    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
    
    def IsAdmin(self):
        return self.grupo == 2
    
    def IsOperator(self):
        return self.grupo == 1
    
    def IsUser(self):
        return self.grupo == 0
    
    def GetBibliotecas(self):
        if self.grupo == 2:
            return Biblioteca.objects.all()
        elif self.grupo == 1:
            operadores=list(Operadores.objects.filter(operador=self))
            ret = []
            for i in operadores:
                ret.append(i.biblioteca)   
            return ret
        
    def GetRandomBooks(self):
        genero = GeneroLivro.objects.filter(perfil=self)[0]
        livros = Livro.objects.filter(genero=genero.tipo)
        livros_aleatorios = random.sample(list(livros), 4)
        return livros_aleatorios
        
    
    #Esse método sobrescreve o save padrão do model, para antes de salvar ele associa o usuário a um grupo
    def save(self, *args, **kwargs):
        if self.grupo == 0:
            my_group = Group.objects.get(name='Usuário') 
            #permissoes = Group
            my_group.user_set.add(self.user)
            self.user.is_superuser = False
            self.user.is_staff = False
            self.user.save()
        elif self.grupo == 1:
            my_group = Group.objects.get(name='Operador') 
            #permissoes = Group
            my_group.user_set.add(self.user)
        elif self.grupo == 2:
            self.user.is_superuser = True
            self.user.is_staff = True
            self.user.save()
        super().save(*args, **kwargs)  # Call the "real" save() method.


class GeneroLivro(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete = models.CASCADE)
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
    tipo = models.IntegerField(choices = genero_choices, default = 0)

    def __str__(self):
        return self.genero_choices[self.tipo][1]
    
class Operadores(models.Model):
    operador = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    biblioteca = models.ForeignKey(Biblioteca, on_delete = models.CASCADE)