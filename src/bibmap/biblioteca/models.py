from django.db import models
import datetime
from django.utils import timezone
from livro.models import Livro
# Create your models here.


class Endereco(models.Model):
    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=256)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=256)
    cidade = models.CharField(max_length=256) 
    estado = models.CharField(max_length=2)
    def __str__(self):
        return "{}, {} - {}, {}/{}".format(self.rua, self.numero, self.bairro, self.cidade, self.estado)


class RecursosOpcionais(models.Model):
    computador = models.BooleanField() 
    ar_condicionado = models.BooleanField()
    mesa_de_estudo = models.BooleanField()
    empresta_livro = models.BooleanField()
    wifi = models.BooleanField()

class Biblioteca(models.Model):
    recursos_opcionais = models.ForeignKey(RecursosOpcionais, on_delete=models.PROTECT, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=True)
    comentario = models.TextField()
    nome = models.CharField(max_length=256)
    foto = models.ImageField(upload_to='images/bib/')
    nome_bibliotecario = models.CharField(max_length=256)
    independente = models.BooleanField()
    aquisicao_acervo = models.BooleanField()
    aberto_a_comunidade = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField("Biblioteca está ativa?", editable=True, default=True)

    #Variável para saber se a biblioteca deu as coordenadas
    mapeada = models.BooleanField()
    latitude = models.DecimalField(max_digits=19, decimal_places=16)
    longitude = models.DecimalField(max_digits=19, decimal_places=15)
    
    
    last_reseted_views = models.DateField(default = datetime.date(2000, 1, 1))
    visualizacoes = models.IntegerField(default=0)
    
    def __str__(self):
        ret = "{}".format(self.nome)
        return ret
    def Serializer(self):
        ret = {
            "nome":self.nome,
            "foto": self.foto.url,
            "endereco": str(self.endereco),
            "id": self.id,
            "visualizacoes": self.visualizacoes,
            "mapeada": self.mapeada,
            "lat": self.latitude,
            "lng": self.longitude
        }
        return ret

class LivroAssociado(models.Model):
    biblioteca = models.ForeignKey(Biblioteca, on_delete = models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete = models.CASCADE)
    status = models.BooleanField(default = True)
    estado_choices = [
        (0, 'Excelente'),
        (1, 'Ótimo'),
        (2, 'Bom'),
        (3, 'Regular'),
        (4, 'Ruim'),
        (5, 'Péssimo'),
    ]
    estado = models.IntegerField(choices = estado_choices, default = 0)
    numero_protocolo = models.IntegerField(default = 0)
    corredor = models.CharField(max_length = 5)
    prateleira = models.CharField(max_length= 5)

    def __str__(self):
        return "{} - {}".format(self.livro, self.biblioteca)
    def LivroCount(self):
        return LivroAssociado.objects.filter(biblioteca=self.biblioteca, livro=self.livro).count()
