from django.db import models
from geopy import distance
from biblioteca.models import Biblioteca
import json
# Create your models here.

class LivroPesquisa():
    nome = ""
    capa = ""
    autores = ""
    genero = ""
    id_livro = None
    quant_disponivel = 0
    menor = 999999999
    id_menor = False
    precisa_estar_disponivel = None
    def ReturnSerializer(self):
        if self.precisa_estar_disponivel:
            if self.quant_disponivel > 0:
                return {
                    "nome":self.nome,
                    "capa":self.capa,
                    "autores":self.autores,
                    "genero":self.genero,
                    "quant_disponivel":self.quant_disponivel,
                    "menor":self.menor,
                    "distancia":self.menor,
                    
                    "id_menor":self.id_menor,
                    "id_livro":self.id_livro
                }
            else: return False
        else:
                return {
                    "nome":self.nome,
                    "capa":self.capa,
                    "autores":self.autores,
                    "genero":self.genero,
                    "quant_disponivel":self.quant_disponivel,
                    "menor":self.menor,
                    "distancia":self.menor,
                    "id_menor":self.id_menor,
                    "id_livro":self.id_livro                    
                }
    def __init__(self, dictin, lng = None, lat= None, disponivel=False):
        
        self.nome = dictin["nome"]
        self.capa = dictin["capa"]
        self.autores = dictin["autores"]
        self.genero = dictin["genero"]
        self.quant_disponivel = dictin["disponivel"].values_list('biblioteca_id', flat=True).distinct().count()
        self.precisa_estar_disponivel = disponivel
        self.id_livro = dictin["id"]
        if lng != None and lat != None:
            listids = list(dictin["disponivel"].values_list('biblioteca_id', flat=True).distinct())
            bibs = Biblioteca.objects.filter(id__in=listids)
            user = (lat, lng)
            for bib in bibs:
                bib_coord = (bib.latitude, bib.longitude)
                distancia = distance.distance(user, bib_coord).km
                if (distancia < self.menor):
                    self.menor = round(distancia, 2)
                    self.id_menor = bib.id
            
    def __str__(self):
        return self.nome
        
        
        
class BibliotecaPesquisa():
    nome = ""
    foto = ""
    endereco = ""
    id_bib = None
    views = None
    distancia = None
    precisa_distancia = False
    def __eq__(self, other):
        if self.distancia != None:
            return self.distancia == other.distancia and self.views == other.views
        else:
            return self.views == self.views

    def __lt__(self, other):
        if self.distancia != None:
            return self.distancia < other.distancia
        else:
            return self.views < self.views
    
    def ReturnSelf(self):
        if self.precisa_distancia:
            if self.distancia != None:
                return self
            else:
                return False
        else:
            return self
        
    
    def ReturnSerializer(self):
        if self.precisa_distancia and self.distancia!= None:
            if self.distancia != None:
                return {
                    "nome":self.nome,
                    "foto":self.foto,
                    "endereco":self.endereco,
                    "id_bib":self.id_bib,
                    "distancia": self.distancia
                    }
            else:
                return False
        else:
            return {
                    "nome":self.nome,
                    "foto":self.foto,
                    "endereco":self.endereco,
                    "id_bib":self.id_bib,
                    "distancia": self.distancia
                                
                    }
    def __init__(self, dictin, lng = None, lat= None, cep=False):
        
        self.nome = dictin["nome"]
        self.foto = dictin["foto"]
        self.endereco = dictin["endereco"]
        self.id_bib = int(dictin["id"])
        self.views = int(dictin["visualizacoes"])
        bib_lat, bib_lng = float(dictin["lat"]), float(dictin["lng"])
        if lng != None and lat != None:
            if cep:
                self.precisa_distancia = True
                lngmax, latmax,lngmin,latmin = float(lng) + 0.045, float(lat)+0.045, float(lng) - 0.045, float(lat) - 0.045
            else:
                lngmax, latmax, lngmin, latmin = 9999,9999,-9999,-9999
            if (latmax>bib_lat and latmin < bib_lat) and (lngmax > bib_lng and lngmin < bib_lng):
                dist = (lat, lng)
                bib_coord = (bib_lat, bib_lng)
                distancia = distance.distance(dist, bib_coord).km
                distancia = round(distancia, 2)
                self.distancia = distancia
                
        
    def __str__(self):
        return self.nome
        