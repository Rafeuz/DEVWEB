from django.shortcuts import render
from .models import Livro
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
import urllib.request
import logging
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from usuario.models import Perfil

logger = logging.getLogger(__name__)

def Existe(livro):
    search = Livro.objects.filter(nome__iexact=livro.nome).filter(isbn_10__iexact=livro.isbn_10).filter(isbn_13__iexact=livro.isbn_13)
    if search:
        return search[0]
    else:
        return False


@login_required
def Adicionar(request): 
    
    perfil = Perfil.objects.get(id = request.session["perfil"])
    if perfil.grupo == 0:
        return render(request, "registration/unauthorized.html")
    
    livro = Livro()
    ### ATRIBUTOS LIVRO
    nome = request.POST["nome"].strip()
    if nome:
        livro.nome = nome
    else:
        return HttpResponseRedirect(reverse('', args=("")))

    isbn_10 = request.POST["isbn_10"].strip()
    if isbn_10:
        livro.isbn_10 = isbn_10
    else:
        return HttpResponseRedirect(reverse('livro:ListarErro', args=("CampoVazio",)))
    
    resumo = request.POST["resumo"].strip()
    if resumo:
        livro.resumo = resumo
    else:
        return HttpResponseRedirect(reverse('livro:ListarErro', args=("CampoVazio",)))
    
    
    isbn_13 = request.POST["isbn_13"].strip()
    if isbn_13:
        livro.isbn_13 = isbn_13
    else:
        return HttpResponseRedirect(reverse('livro:ListarErro', args=("CampoVazio",)))

    editora = request.POST["editora"].strip()
    if editora:
        livro.editora = editora
    else:
        return HttpResponseRedirect(reverse('livro:ListarErro', args=("CampoVazio",)))

    livro.genero = request.POST.get('genero', default=0)
    livro.status = True

    
    if Existe(livro):
        return HttpResponseRedirect(reverse('livro:ListarErro', args=("LivroExistente",)))
    else:
        linkfoto = request.POST["linkfoto"].strip()
        if request.FILES:
            logger.error(request.FILES)
            livro.capa = request.FILES["foto"]
        else:
            if linkfoto:
                media_root = settings.MEDIA_ROOT
                media_root = os.path.join(media_root, "images", "livros")                
                file_name = "{}-{}.png".format(livro.nome, livro.isbn_10)
                path = os.path.join(media_root, file_name)
                urllib.request.urlretrieve(linkfoto, path)
                livro.capa="images/livros/{}".format(file_name)
            else:
                media_root = settings.MEDIA_ROOT
                media_root = os.path.join(media_root, "images", "livros")                
                file_name = "{}-{}.png".format(livro.nome, livro.isbn_10)
                path = os.path.join(media_root, file_name)               
                urllib.request.urlretrieve('http://www.guiada3aidade.com.br/wp-content/uploads/2018/10/sem-capa.jpg', path)
                livro.capa="images/livros/{}".format(file_name)
        
        
        autores = request.POST.get("Autores", ";").split(";")
        livro.autor=""
        flag = False
        aux = []
        for autor in autores:
            if autor.strip():
                aux.append(autor.strip())
                flag = True
        if not flag:
            return HttpResponseRedirect(reverse('livro:ListarErro', args=("CampoVazio",)))
        livro.autor = ";".join(aux)
        livro.save()
    return HttpResponseRedirect(reverse('livro:ListarErro', args=("CadastradoComSucesso",)))

@login_required
def ListarSingle(request, livro_id=None, erro=None):
    perfil = Perfil.objects.get(id = request.session["perfil"])
    if perfil.grupo == 0:
        return render(request, "registration/unauthorized.html")
    
    
    try:
        if request.POST["id"]:
            livro_id = request.POST["id"]
    except:
        pass
    livro = get_object_or_404(Livro, pk=livro_id)
    context = { "livro": livro, "erro": erro }
    context["perfil"] = perfil    
    return render(request, 'livros/livro_visualizar.html', context)

@login_required
def Editar(request, livro_id=None):
    perfil = Perfil.objects.get(id = request.session["perfil"])
    if perfil.grupo == 0:
        return render(request, "registration/unauthorized.html")
    
    try:
        if request.POST["id"]:
            livro_id = request.POST["id"]
    except:
        pass
    livro = get_object_or_404(Livro, pk=livro_id)
    nome = request.POST["nome"].strip()
    if nome:
        livro.nome = nome
    else:
        return HttpResponseRedirect(reverse('livro:ListarErro', args=("CampoVazio",)))

    isbn_10 = request.POST["isbn_10"].strip()
    
    if isbn_10:
        livro.isbn_10 = isbn_10
    else:
        return HttpResponseRedirect(reverse('livro:ListarErro', args=("CampoVazio",)))

    isbn_13 = request.POST["isbn_13"].strip()
    if isbn_13:
        livro.isbn_13 = isbn_13
    else:
        return HttpResponseRedirect(reverse('livro:ListarErro', args=("CampoVazio",)))

    editora = request.POST["editora"].strip()
    if editora:
        livro.editora = editora
    else:
        return HttpResponseRedirect(reverse('livro:ListarErro', args=("CampoVazio",)))

    livro.genero = request.POST.get('genero', default=0)

    resumo = request.POST["resumo"].strip()
    if resumo:
        livro.resumo = resumo
    else:
        return HttpResponseRedirect(reverse('livro:ListarErro', args=("CampoVazio",)))

    autores =[]
    autores = request.POST.get("Autores", ";").split(";")
    livro.autor=""
    flag = False
    for autor in autores:
        if autor.strip():
            livro.autor += autor
            flag = True
    if not flag:
        return HttpResponseRedirect(reverse('livro:ListarErro', args=("CampoVazio",)))
    existe = Existe(livro)
    if existe and existe.id!=livro.id:
        return HttpResponseRedirect(reverse('livro:ListarErro', args=("LivroExistente",)))
    else:
        if request.FILES:
            livro.capa.delete()
            livro.capa = request.FILES["foto"]
        livro.save() 
    return HttpResponseRedirect(reverse('livro:listar'))
    
@login_required
def Listar(request, erro = None):
    perfil = Perfil.objects.get(id = request.session["perfil"])
    if perfil.grupo == 0:
        return render(request, "registration/unauthorized.html")
    
    livros = Livro.objects.all()
    context = {}
    if erro == None:
        if livros:
            context = { "livros": livros, "error_message": "", }
        else:
            context = { "livros": [], "error_message": "Nenhum livro cadastrado", }

    elif erro == "CampoVazio":
        if livros:
            context = { "livros": livros, "error_message": "", }
        else:
            context = { "livros": livros,
                      "error_message": "Nenhum livro cadastrado", 
                      "error_message2": "Por favor preencha todos os campos" }
    
    elif erro == "LivroExistente":
        if livros:
            context = { "livros":livros,                         
                       "error_message": "",
                       "error_message2": "Livro já cadastrado", }
        else:
            context = { "livros": [],                      
                       "error_message": "Nenhum livro cadastrado",
                       "error_message2": "Livro já cadastrado", }
    
    elif erro == "IsbnInvalido":
        if livros:
            context = { "livros":livros,                      
                       "error_message": "",
                       "error_message2": "Por favor forneca um ISBN válido", }
        else:
            context = { "livros": [],
                        "error_message": "Nenhum livro cadastrado",
                        "error_message2": "Por favor forneca um ISBN válido", }
    
    elif erro == "CadastradoComSucesso":
        context = { "livros": livros,
                    "error_message": "",
                    "success_message": "Livro cadastrado com sucesso", }
    context["perfil"] = perfil    
    return render(request, 'livros/livros_listar.html', context)

@login_required
def MudarStatus(request, livro_id = None):
    perfil = Perfil.objects.get(id = request.session["perfil"])
    if perfil.grupo != 2:
        return render(request, "registration/unauthorized.html")    
    livro = get_object_or_404(Livro, pk=livro_id)
    livro.status = (not livro.status) #Inverte o status de livro
    livro.save()
    return HttpResponseRedirect(reverse("livro:listar"))

