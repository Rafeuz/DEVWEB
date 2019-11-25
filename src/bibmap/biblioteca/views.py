from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Biblioteca
from .models import Endereco
from .models import RecursosOpcionais
from .models import LivroAssociado 
from livro.models import Livro
from django.template import loader
from django.urls import reverse
from django.views import generic
from random import randint
import datetime
import logging 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from usuario.models import Operadores, Perfil
from django.contrib import messages
from PIL import Image


# Create your views here.
logger = logging.getLogger(__name__)
def testeimagem(request, bibid):
    b = get_object_or_404(Biblioteca, pk=bibid)
    return render(request, "biblioteca/teste_imagem.html", {"bib": b})

#To do#
def Existe(bib, endereco):
    search = Biblioteca.objects.filter(nome__iexact=bib.nome).filter(endereco__cep__iexact=endereco.cep).filter(endereco__numero__iexact=endereco.numero)
    if search:
        return search[0]
    else:
        return False

@login_required
def ListarSingle(request, bibid = None):
    try:
        if request.POST["id"]:
            bibid = request.POST["id"]
    except:
        pass
    b = get_object_or_404(Biblioteca, pk=bibid)
    livros = Livro.objects.all()
    
    #Verificando se o perfil logado está associado a biblioteca ou é admin
    perfil = Perfil.objects.get(id = request.session["perfil"])
    operadores = Operadores.objects.filter(operador=perfil, biblioteca=b)
    if not operadores and perfil.grupo != 2:
        return render(request, "registration/unauthorized.html", context={"perfil": perfil})
    context =   { "b": b,
                  "livros": livros
                }
    if (request.session.pop("acervo", False)):
        context["flag"] = "true"
    context["perfil"] = perfil
    return render(request, "biblioteca/biblioteca_visualizar.html", context)


@login_required
def Editar(request, bibid=None):
    try:
        if request.POST["id"]:
            bibid = request.POST["id"]
    except:
        pass
    bib = get_object_or_404(Biblioteca, pk=bibid)
    
    perfil = Perfil.objects.get(id = request.session["perfil"])
    operadores = Operadores.objects.filter(operador=perfil, biblioteca=bib)
    if not operadores and perfil.grupo != 2:
        return render(request, "registration/unauthorized.html", context={"perfil": perfil})        

    endereco = Endereco.objects.get(pk=bib.endereco.id)
    recursos = RecursosOpcionais.objects.get(pk=bib.recursos_opcionais.id)


    ######## ATRIBUTOS DE BIBLIOTECA ########
    nome = request.POST["nome"].strip() #Deleta todos os caracteres vazios da string

    if nome: #Checa se a string é vazia
        bib.nome = nome
    else:
        messages.add_message(request, messages.WARNING, 'Por favor preencha todos os campos')     
        return HttpResponseRedirect(reverse('biblioteca:ListarSingle', args=(bibid,)))
    
    nome_bibliotecario = request.POST["nome_bibliotecario"].strip() #Checa se a string é vazia
    
    if nome_bibliotecario:
        bib.nome_bibliotecario = nome_bibliotecario
    else:
        messages.add_message(request, messages.WARNING, 'Por favor preencha todos os campos')     
        return HttpResponseRedirect(reverse('biblioteca:ListarSingle', args=(bibid,)))
    bib.independente = request.POST.get('independente',default=False)
    bib.aquisicao_acervo = request.POST.get('aquisicao_acervo',default=False)
    bib.aberto_a_comunidade = request.POST.get('aberto_a_comunidade',default=False)
    bib.status = request.POST.get('status', default=False)
    bib.comentario = request.POST.get("comentario", default="")
    if request.FILES:
        bib.foto.delete()
        bib.foto = request.FILES["foto"]
    ######## FIM ATRIBUTOS DE BIBLIOTECA ########
    
    ########    ATRIBUTOS DE ENDEREÇO    ########
    cep = request.POST["cep"].strip()
    if cep:
        endereco.cep = cep
    else:
        messages.add_message(request, messages.WARNING, 'Por favor preencha todos os campos')     
        return HttpResponseRedirect(reverse('biblioteca:ListarSingle', args=(bibid,)))
    endereco.rua = request.POST["rua"]
    num = request.POST["numero"].strip() #Checa se a string é vazia
    if num:
        endereco.numero = num
    else:
        messages.add_message(request, messages.WARNING, 'Por favor preencha todos os campos')     
        return HttpResponseRedirect(reverse('biblioteca:ListarSingle', args=(bibid,)))
    endereco.bairro = request.POST["bairro"] #Checa se a string é vazia
    endereco.estado = request.POST["estado"]
    endereco.cidade = request.POST["cidade"]
    
    ######## FIM ATRIBUTOS DE ENDEREÇO ########
    
    #😠😠😠😠😠😠    ATRIBUTOS DE RECURSOS    😠😠😠😠😠😠#
    recursos.computador = request.POST.get('computador',default=False)
    recursos.mesa_de_estudo = request.POST.get('mesa_de_estudo',default=False)
    recursos.empresta_livro = request.POST.get('empresta_livro',default=False)
    recursos.ar_condicionado = request.POST.get('ar_condicionado',default=False)
    recursos.wifi = request.POST.get('wifi',default=False)

    
    existe = Existe(bib, endereco)
    if existe != False:
        if existe.id == bib.id:
            logger.error("entrou aqui")
            endereco.save()
            recursos.save()
            bib.endereco = endereco
            bib.recursos_opcionais = recursos
        else:
            messages.add_message(request, messages.ERROR, 'Biblioteca existente')
            return HttpResponseRedirect(reverse('biblioteca:ListarSingle', args=(bibid,)))
    bib.save()
    if request.FILES:
        bib.foto = request.FILES["foto"]
        bib.save()
        x = float(request.POST['x'])
        y = float(request.POST['y'])
        width = float(request.POST['width'])
        height = float(request.POST['height'])
        # A partir daqui a foto será alterada pra ficar em proporção 1:1
        im = Image.open(bib.foto) # Abrir a foto
        im = im.crop((x, y, x+width, y+height))
        im.save(bib.foto.path, quality=100)
    messages.add_message(request, messages.SUCCESS, 'Biblioteca editada com sucesso')     
    return HttpResponseRedirect(reverse('biblioteca:ListarSingle', args=(bibid,)))

@login_required
def Adicionar(request):
    bib = Biblioteca()
    endereco = Endereco()
    recursos = RecursosOpcionais()
    perfil = Perfil.objects.get(id = request.session["perfil"])
    if perfil.grupo != 2:
        return render(request, "registration/unauthorized.html", context={"perfil": perfil})
    ######## ATRIBUTOS DE BIBLIOTECA ########
    nome = request.POST["nome"].strip() #Deleta todos os caracteres vazios da string

    if nome: #Checa se a string é vazia
        bib.nome = nome
    else:
        messages.add_message(request, messages.WARNING, 'Por favor preencha todos os campos')     
        return HttpResponseRedirect(reverse('biblioteca:listar'))
    
    nome_bibliotecario = request.POST["nome_bibliotecario"].strip() #Checa se a string é vazia
    
    if nome_bibliotecario:
        bib.nome_bibliotecario = nome_bibliotecario
    else:
        messages.add_message(request, messages.WARNING, 'Por favor preencha todos os campos')     
        return HttpResponseRedirect(reverse('biblioteca:listar'))
    bib.independente = request.POST.get('independente',default=False)
    bib.aquisicao_acervo = request.POST.get('aquisicao_acervo',default=False)
    bib.aberto_a_comunidade = request.POST.get('aberto_a_comunidade',default=False)
    bib.status = request.POST.get('status',default=False)
    bib.comentario = request.POST.get("comentario", default="")
    if request.FILES:
        bib.foto = request.FILES["foto"]
    ######## FIM ATRIBUTOS DE BIBLIOTECA ########
    
    ########    ATRIBUTOS DE ENDEREÇO    ########
    cep = request.POST["cep"].strip()
    if cep:
        endereco.cep = cep
    else:
        messages.add_message(request, messages.WARNING, 'Por favor preencha todos os campos')     
        return HttpResponseRedirect(reverse('biblioteca:listar'))
    endereco.rua = request.POST["rua"]
    num = request.POST["numero"].strip() #Checa se a string é vazia
    if num:
        endereco.numero = num
    else:
        messages.add_message(request, messages.WARNING, 'Por favor preencha todos os campos')     
        return HttpResponseRedirect(reverse('biblioteca:listar'))
    endereco.bairro = request.POST["bairro"] #Checa se a string é vazia
    endereco.estado = request.POST["estado"]
    endereco.cidade = request.POST["cidade"]
    
    ######## FIM ATRIBUTOS DE ENDEREÇO ########
    
    #😠😠😠😠😠😠    ATRIBUTOS DE RECURSOS    😠😠😠😠😠😠#

    recursos.computador = request.POST.get('computador',default=False)
    recursos.mesa_de_estudo = request.POST.get('mesa_de_estudo',default=False)
    recursos.empresta_livro = request.POST.get('empresta_livro',default=False)
    recursos.ar_condicionado = request.POST.get('ar_condicionado',default=False)
    recursos.wifi = request.POST.get('wifi',default=False)

    latitude = request.POST.get('lat',default=False)
    longitude = request.POST.get('lng',default=False)
    if not latitude or not longitude:
        bib.latitude = 0
        bib.longitude = 0
        bib.mapeada = False
    else:
        bib.latitude = request.POST['lat']
        bib.longitude = request.POST['lng']
        bib.mapeada = True
    existe = Existe(bib, endereco)
    if not existe:
        endereco.save()
        recursos.save()
        bib.endereco = endereco
        bib.recursos_opcionais = recursos
    else:
        if existe.status:
            messages.add_message(request, messages.ERROR, 'A biblioteca já está cadastrada')     
            return HttpResponseRedirect(reverse('biblioteca:listar'))
        else:
            existe.status = True
            existe.save()
            messages.add_message(request, messages.SUCCESS, 'A biblioteca já estava cadastrada e apenas foi ativada')     
        return HttpResponseRedirect(reverse('biblioteca:listar'))

    
    bib.save()
    if request.FILES:
        bib.foto = request.FILES["foto"]
        bib.save()
        x = float(request.POST['x'])
        y = float(request.POST['y'])
        width = float(request.POST['width'])
        height = float(request.POST['height'])
        messages.add_message(request, messages.SUCCESS, 'Sua foto foi alterada com sucesso')    
        # A partir daqui a foto será alterada pra ficar em proporção 1:1
        im = Image.open(bib.foto) # Abrir a foto
        im = im.crop((x, y, x+width, y+height))
        im.save(bib.foto.path, quality=100)
        
    messages.add_message(request, messages.SUCCESS, 'Biblioteca cadastrada com sucesso')     
    return HttpResponseRedirect(reverse('biblioteca:listar'))

@login_required
def Listar(request):
    
    
    perfil = Perfil.objects.get(id = request.session["perfil"])
    if perfil.grupo == 2:
        bibs = Biblioteca.objects.all() #Retorna todas as bibliotecas caso seja admin
    elif perfil.grupo == 1:
        bibs = perfil.GetBibliotecas() #Retorna apenas as bibliotecas associadas ao operador
    else:
        return render(request, "registration/unauthorized.html", context={"perfil": perfil})
    context = {"b":bibs,}
    context["perfil"] = perfil
    context["bibmap"] = 'placeholder'
    return render(request, 'biblioteca/biblioteca_listar.html', context)

@login_required
def MudarStatus(request, bibid = None):
    bib = get_object_or_404(Biblioteca, pk=bibid)
    bib.status = (not bib.status) #Inverte o status da biblioteca
    bib.save()
    return HttpResponseRedirect(reverse("biblioteca:listar"))


@login_required
def AssociarLivroBiblioteca(request, biblioteca_id):
    request.session["acervo"] = True
    #Recupera no banco a biblioteca solicitada
    biblioteca = get_object_or_404(Biblioteca, pk = biblioteca_id)
    
    perfil = Perfil.objects.get(id = request.session["perfil"])
    operadores = Operadores.objects.filter(operador=perfil, biblioteca=biblioteca)
    if not operadores and perfil.grupo != 2:
        return render(request, "registration/unauthorized.html", context={"perfil": perfil})

    
    livro_id = request.POST["livro_id"].strip() #Deleta todos os caracteres vazios da string
    #Recupera no banco o livro solicitado
    livro = get_object_or_404(Livro, pk = livro_id)
    #Recebe a quantidade de livros a ser criada
    quantidade_de_livros = int(request.POST["quantidade"])
    estado = int(request.POST["estado"])
    #Recebe os atributos para localização física do livro
    corredor = request.POST["corredor"].strip() #Deleta todos os caracteres vazios da string
    prateleira = request.POST["prateleira"].strip() #Deleta todos os caracteres vazios da string

    if quantidade_de_livros < 1:
        messages.add_message(request, messages.ERROR, 'Quantidade de livros inválida')     
        return HttpResponseRedirect(reverse('biblioteca:ListarSingle', args=(biblioteca_id,)))
    elif not corredor or not prateleira:
        messages.add_message(request, messages.WARNING, 'Por favor preencha todos os campos')     
        return HttpResponseRedirect(reverse('biblioteca:ListarSingle', args=(biblioteca_id,)))
    else:
        #Utiliza um laço pra criar a quantidade de livros informada
        for i in range(0, quantidade_de_livros):
            #Cria um novo livro associado
            livro_associado = LivroAssociado()
            #Relaciona a entidade livro_da_biblioteca com a biblioteca e livro escolhidos
            livro_associado.biblioteca = biblioteca
            livro_associado.livro = livro
            #Preenche os atributos que identificam o livro associado        
            livro_associado.estado = estado
            livro_associado.corredor = corredor
            livro_associado.prateleira = prateleira
            #Gera um número único para cada livro associado (biblioteca_id + livro_id + ano + mes + dia + numero aleatorio)
            livro_associado.numero_protocolo = int("{}{}{}{}{}{}".format(biblioteca_id, livro_id, datetime.date.today().year, datetime.date.today().month, datetime.date.today().day, randint(0, 999)))
            livro_associado.save()

    return redirect(reverse('biblioteca:ListarSingle', args=[biblioteca.id]))

@login_required
def EditarLivroAssociado(request, livroassociado_id):
    request.session["acervo"] = True
    livro_associado = LivroAssociado.objects.get(pk = livroassociado_id)
    estado = int(request.POST["estado"])
    #Recebe os atributos para localização física do livro
    corredor = request.POST["corredor"].strip() #Deleta todos os caracteres vazios da string
    prateleira = request.POST["prateleira"].strip() #Deleta todos os caracteres vazios da string

    if not estado or not corredor or not prateleira:
        messages.add_message(request, messages.WARNING, 'Por favor preencha todos os campos')     
        return HttpResponseRedirect(reverse('biblioteca:ListarSingle', args=(livro_associado.biblioteca.id,)))
    else:
        livro_associado.estado = estado
        livro_associado.corredor = corredor
        livro_associado.prateleira = prateleira

    livro_associado.save()

    return redirect(reverse('biblioteca:ListarSingle', args=[livro_associado.biblioteca.id]))

@login_required
def EditarStatusLivroAssociado(request, livroassociado_id):
    request.session["acervo"] = True
    livro_associado = LivroAssociado.objects.get(pk = livroassociado_id)
    perfil = Perfil.objects.get(id = request.session["perfil"])
    operadores = Operadores.objects.filter(operador=perfil, biblioteca=livro_associado.biblioteca)
    if not operadores and perfil.grupo != 2:
        return render(request, "registration/unauthorized.html", context={"perfil": perfil})

    livro_associado.status = not livro_associado.status

    livro_associado.save()

    return redirect(reverse('biblioteca:ListarSingle', args=[livro_associado.biblioteca.id]))