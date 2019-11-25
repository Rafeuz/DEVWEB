from django.shortcuts import render, get_object_or_404
from livro.models import Livro
from biblioteca.models import Biblioteca, LivroAssociado
from accounts.models import LivroUsuario
from usuario.models import Perfil
import random
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponse
from .models import LivroPesquisa, BibliotecaPesquisa
import requests
import json
import math
def index(request):
    return render(request, 'home/home.html')

def GetCepLatLng(cep):
    header = { 'sessionid': '123..'}
    src = requests.get('https://nominatim.openstreetmap.org/search.php?q=' + cep, header).text
    src = src.split("<footer>")[0]
    src = src.split('<script type="text/javascript">')
    src = src[len(src)-1]
    src = src.split('\n')
    obj = {}
    for i in range(len(src)-1, 0, -1):
        if 'lat' in src[i]:
            obj["lat"] = src[i].split('"')[3]
        elif 'lon' in src[i]:
            obj["lng"] = src[i].split('"')[3]
            
        if 'nominatim_results' in src[i]:
            break
    if obj == {}:
        obj["lat"] = None
        obj["lng"] = None
    return obj


def listarLivrosBibliotecas(request):
    livros = Livro.objects.filter(status=True).order_by('-visualizacoes')[:4]
    bibliotecas_mapeadas = Biblioteca.objects.filter(mapeada=True)
    ultimas_bibliotecas = Biblioteca.objects.filter(status=True).order_by('-id')[:4] #Pegando as 4 últimas bibliotecas cadastradas atraves do id
    context = {'livros_aleatorios': livros, 'ultimas_bibliotecas': ultimas_bibliotecas, "bibmap": bibliotecas_mapeadas}
    return render(request, 'home/home.html', context)
    
def visualizarLivro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    bibs_ids = LivroAssociado.objects.filter(livro=livro).values_list('biblioteca_id', flat=True).distinct() #Pegando os IDs de todas as bibliotecas associadas ao livro e removendo as repetidas
    bibs_associadas = Biblioteca.objects.filter(id__in=bibs_ids).order_by('-visualizacoes') #Pegando as bibliotecas que possuem um ID em bibs_ids    
    livrousuario = LivroUsuario.objects.filter(livro = livro) #Retorna todos as relações desse livro com usuarios
    if (timezone.now().date() > livro.last_reseted_views + timedelta(days=6)):
        livro.last_reseted_views = timezone.now().date()
        livro.visualizacoes= 0
    livro.visualizacoes+=1
    livro.save()
    context = {'livro': livro, 'bibs_associadas': bibs_associadas, 'bibmap': bibs_associadas, 'livrousuario': livrousuario,}
    return render(request, 'home/visualizar_livro.html', context)

def visualizarBiblioteca(request, biblioteca_id):
    #try:
    biblioteca = get_object_or_404(Biblioteca, pk=biblioteca_id)
    if (timezone.now().date() > biblioteca.last_reseted_views + timedelta(days=6)):
        biblioteca.last_reseted_views = timezone.now().date()
        biblioteca.visualizacoes= 0
    biblioteca.visualizacoes+=1
    biblioteca.save()
    livros = LivroAssociado.objects.filter(biblioteca=biblioteca)
    quantidade_livros = len(list(livros))
    livros_ids = list(livros.values_list('livro__id', flat=True).distinct())#Pegando os IDs de todos os livros associados a biblioteca e removendo os repetidos
    #livros_associados = Livro.objects.filter(id__in=livros_ids) #Pegando os livros que possuem um ID em livros_ids
    #except:
        #pass
    livros_associados = []
    for i in livros_ids:
        livros_associados.append(LivroAssociado.objects.filter(livro__id = i, biblioteca = biblioteca)[0])

    context = {'biblioteca':biblioteca, 'livros_associados': livros_associados, 'quantidade_livros':quantidade_livros }
    context['bibmap'] = [biblioteca]
    return render(request, 'home/visualizar_biblioteca.html', context)

def PaginaPesquisa(request):
    return render(request, "home/pesquisa.html")

def Pesquisa(request, page=1):
    
    #Livros
    filtroAutor = request.GET.get("autor", "").strip().lower()
    pesquisa_isbn = request.GET.get("isbn", "").strip()
    somente_associados = request.GET.get("associados", False)
    somente_associados = bool(somente_associados)
    
    
    #campos gerais
    lat, lng = request.GET.get("lat", None), request.GET.get("lng", None) #Coordenadas do usuario
    resultados_de = request.GET.get("resultados", "all") #Mostrar resultado de
    simples = request.GET.get("search", "").strip() #Busca textual
    
    parameters = {
        'mostrar': resultados_de,
        'somente_associados': somente_associados,
        'search' : simples
    }
    #Campos de filtro de biblioteca
    cep = request.GET.get("cep", False)
    
    independente = request.GET.get("independente", False)
    independente = bool(independente)
    
    computadores = request.GET.get("computadores", False)
    computadores = bool(computadores)
    
    aberta_a_comunidade = request.GET.get("aberta_a_comunidade", False)
    aberta_a_comunidade = bool(aberta_a_comunidade)
    
    emprestimos = request.GET.get("emprestimos", False)
    emprestimos = bool(emprestimos)
    
    acervo_proprio = request.GET.get("acervo_proprio", False)
    acervo_proprio = bool(acervo_proprio)

    max_dist = request.GET.get("distanciainput", '')
    max_dist = max_dist.strip()
    if max_dist:
        max_dist = float(max_dist)
        parameters['max_dist'] = math.ceil(max_dist)
    else:
        max_dist = 999999999
        parameters['max_dist'] = ''
    
    ac = request.GET.get("ac", False)
    ac = bool(ac)
    
    wifi = request.GET.get("wifi", False)
    wifi = bool(wifi)
    
    mesa_de_estudo = request.GET.get('mesa_de_estudo', False)
    mesa_de_estudo = bool(mesa_de_estudo)
    
    getParams = []
    
    getParams+= ["max_dist:"+ str(max_dist)]
    
        
    if independente:
        getParams+= ["independente"]
        parameters['independente'] = independente;
    if computadores:
        getParams += ["computadores"]
        parameters['computadores'] = computadores;
    if aberta_a_comunidade:
        getParams += ["aberta_a_comunidade"]
        parameters['aberta_a_comunidade'] = aberta_a_comunidade;
    if emprestimos:
        getParams+=['emprestimos']
        parameters['emprestimos'] = emprestimos;
    if acervo_proprio:
        getParams+=["acervo_proprio"]
        parameters['acervo_proprio'] = acervo_proprio;
    if ac:
        getParams+= ['ac']
        parameters['ac'] = ac;
    if simples:
        getParams+= [simples]
        parameters['simples'] = simples;
        
    if lat and lng:
        getParams += [lat, lng]
    if filtroAutor:
        getParams += [filtroAutor]
        parameters['filtroAutor'] = filtroAutor;
        
    if pesquisa_isbn:
        getParams += [pesquisa_isbn]
        parameters['pesquisa_isbn'] = pesquisa_isbn;
        
    if somente_associados:
        getParams += ["associado"]
    if cep:
        getParams+=["cep=" + cep]
        coord_cep = GetCepLatLng(cep)
        parameters["cep"] = cep
    if mesa_de_estudo:
        getParams += ["mesa_de_estudo"]
        parameters["mesa_de_estudo"] = mesa_de_estudo
        
    if wifi:
        getParams += ["wifi"]
        parameters["wifi"] = wifi
        
    getParams = "&".join(getParams)
    lista_autores = []
    if "search" in request.session and request.session["search"]["termo"] == simples and request.session["search"]["getParams"] == getParams:
               
        resultado_livros = request.session["search"]["resultadoslivros"]
        resultado_bibs = request.session["search"]["resultadosbibliotecas"]
        lista_autores = request.session["search"]["autores"]
    else:
        # Pesquisa de Livros
        if not pesquisa_isbn:
            result_isbn10 = Livro.objects.filter(isbn_10__icontains=simples)
            result_isbn13 = Livro.objects.filter(isbn_13__icontains=simples)
            result_nome = Livro.objects.filter(nome__icontains=simples)
        else:
            result_isbn10 = Livro.objects.filter(isbn_10__icontains=pesquisa_isbn)
            result_isbn13 = Livro.objects.filter(isbn_13__icontains=pesquisa_isbn)
            result_nome = Livro.objects.none()
        if not filtroAutor:
            result_autores = Livro.objects.filter(autor__icontains=simples)
        else:
            result_autores = Livro.objects.filter(autor__icontains=filtroAutor)
        result = result_isbn10.union(result_isbn13, result_nome)
   
        if filtroAutor:
            result = result.intersection(result_autores)
        result = result.order_by('-visualizacoes')            
        result = list(result)
        autores = list(result_autores)
        for i in autores:
            try:
                index = result.index(i)
                if index > 0:
                    result[index], result[index-1] =  result[index-1], result[index]
            except:
                pass
        resultado_livros = []
        for i in result:
            livroPesquisa = LivroPesquisa(i.Serializer(), lng, lat, somente_associados).ReturnSerializer()
            if livroPesquisa and livroPesquisa["menor"] < max_dist:
                resultado_livros.append(livroPesquisa)
                lista_autores += livroPesquisa["autores"]
        #Pesquisa de bibliotecas
        bibs = Biblioteca.objects.filter(status=True)
        bibs = bibs.filter(nome__icontains=simples)
        if wifi:
            bibs = bibs.filter(recursos_opcionais__wifi=True)
        if independente:
            bibs = bibs.filter(independente = True)
        if computadores:
            bibs = bibs.filter(recursos_opcionais__computador=True)
        if ac:
            bibs = bibs.filter(recursos_opcionais__ar_condicionado=True)
        if emprestimos:
            bibs = bibs.filter(recursos_opcionais__empresta_livro=True)
        if aberta_a_comunidade:
            bibs = bibs.filter(aberto_a_comunidade=True)
        if mesa_de_estudo:
            bibs = bibs.filter(recursos_opcionais__mesa_de_estudo=True)
            
        resultado_bibs = []
        resultado_bibstemp = []
        if cep:
            for i in bibs:
                bibPesquisa = BibliotecaPesquisa(i.Serializer(), lng=coord_cep["lng"], lat=coord_cep["lat"], cep=True).ReturnSelf()
                if bibPesquisa and bibPesquisa["distancia"] < max_dist:
                    resultado_bibstemp.append(bibPesquisa)
            resultado_bibstemp = sorted(resultado_bibstemp)
            for i in (resultado_bibstemp):
                resultado_bibs.append(i.ReturnSerializer())
        else:
            for i in bibs:
                bibPesquisa = BibliotecaPesquisa(i.Serializer(), lng=lng, lat=lat, cep=False).ReturnSerializer()
                if bibPesquisa and bibPesquisa["distancia"] < max_dist:
                    resultado_bibs.append(bibPesquisa)
        request.session["search"] = {"termo": simples, "resultadoslivros": resultado_livros,"resultadosbibliotecas":resultado_bibs, "getParams": getParams, "autores": lista_autores}
        
    raw_livros = resultado_livros
    raw_bibs = resultado_bibs
    resultado_livros = resultado_livros[(page-1)*15:(page-1)*15+15]
    resultado_bibs = resultado_bibs[(page-1)*15:(page-1)*15+15]
    
    
    lista_autores = sorted(list(set(lista_autores)))
    context = {}
    if resultados_de == "all":
        context["resultados_bibs"] = resultado_bibs
        context["autores"] = lista_autores
        context["resultado_livros"] = resultado_livros
        context["hasnext"] =  len(raw_bibs) > (page-1)*15+15 or len(raw_livros) > (page-1)*15+15
    elif resultados_de == "bibs":
        context["resultados_bibs"] = raw_bibs
        context["autores"] = []
        context["resultado_livros"] = []
        context["hasnext"] = len(raw_bibs) > (page-1)*15+15
        
    else:
        context["resultados_bibs"] = []
        context["autores"] = lista_autores
        context["resultado_livros"] = resultado_livros
        context["hasnext"] = len(raw_livros) > (page-1)*15+15
        
    context['parameters'] = parameters
    context["hasprev"] = page>1
    context["nextpage"] = page+1
    context["prevpage"] = page-1
    #return JsonResponse(context, safe=False)
    return render(request, "home/pesquisa.html", context=context)
    
def listarLivros(request):
    livros = Livro.objects.filter(status=True).order_by('nome')
    context = {'livros': livros }
    return render(request, 'home/listar_livros.html', context)

def listarBibliotecas(request):
    bibliotecas = Biblioteca.objects.filter(status=True).order_by('nome')
    context = {'bibliotecas': bibliotecas}
    return render(request, 'home/listar_bibliotecas.html', context)