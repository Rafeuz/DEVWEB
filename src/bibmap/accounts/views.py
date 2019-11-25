from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from usuario.models import Perfil, Endereco, Telefone, GeneroLivro
from livro.models import Livro
from .models import LivroUsuario, TrocaLivro
from PIL import Image
import os
import urllib
import datetime

def trylogin(request):
    username = request.POST["user"].lower()
    pswd = request.POST["pwd"]
    user = authenticate(username = username, password = pswd)
    print(user)
    next = request.GET.get("next", "")
    if user is not None:
        login(request, user)
        request.session["perfil"] = Perfil.objects.get(user=user).id
        if (next):
            print(next)
            return redirect(next)
        else:
            return redirect(reverse('home:index'))
    else:
        messages.add_message(request, messages.WARNING, 'Os dados inseridos são inválidos')        
        if next:
            return redirect('{}?next={}'.format(settings.LOGIN_URL, next))
        else:
            return redirect('{}'.format(settings.LOGIN_URL))
        
def trylogout(request):
    request.session.pop('perfil', '0')
    if (request.user):
        logout(request)
    next = request.GET.get("next", '')
    if next:
        return redirect(next)
    return redirect(reverse("home:index"))

@login_required
def EditarFoto(request):
    perfil = Perfil.objects.get(id=request.session['perfil'])
    if perfil.foto:
        perfil.foto.delete()
    foto = request.FILES['foto']
    perfil.foto = foto
    perfil.save()
    ret = {'success': True,
           'newUrl': perfil.foto.url
           }
    return JsonResponse(ret)

def Cadastrar(request):
    #Verifica se já existe uma conta de user com o username passado no formulário
    verifica_username = User.objects.filter(username = request.POST['username'].lower().strip()).exists()
    verifica_email = User.objects.filter(email = request.POST['email'].lower().strip())
    flag = False
    
    tentativa_de_cadastro = {
        'nome':'',
        'sobrenome': '',
        'usuario': '',
        'email':'',
        'telefone':'',
        'flag': False
    }
    #Se existir o context ira repassar uma mensagem de erro e impedir a tentativa de criar um user com username já cadastrado
    if verifica_username:
        tentativa_de_cadastro['email'] = request.POST['email'].lower().strip()
        tentativa_de_cadastro['usuario'] = request.POST['username'].lower().strip()
        messages.add_message(request, messages.ERROR, 'Usuário já existente')
        flag = True
    if verifica_email:
        tentativa_de_cadastro['email'] = request.POST['email'].lower().strip()
        tentativa_de_cadastro['usuario'] = request.POST['username'].lower().strip()
        if not flag: messages.add_message(request, messages.ERROR, 'Email já cadastrado')
        flag = True
    #Se não existir um novo user será criado
    else:
        #Recebe as informações mais básicas do usuário, todas obrigatorias
        first_name = request.POST.get('first_name', False).strip()
        last_name = request.POST.get('last_name', False).strip()
        email = request.POST.get('email', False).strip().lower()
        username = request.POST.get('username', False).strip().lower()
        password = request.POST.get('password', False).strip()
        tentativa_de_cadastro['nome'] = request.POST['first_name'].strip()
        tentativa_de_cadastro['sobrenome'] = request.POST['last_name'].strip()
        #Se algumas delas estiver em branco, o cadastro será impedido
        
        #Cria a entidade perfil
        perfil = Perfil()
        #Recebe o atributo sexo, tambem obrigatorio
        sexo = request.POST.get('sexo', False)

        #Se estiver em branco o cadastro é cancelado
        if sexo:
            #Caso não seja, o mesmo é atribuido a entidade perfil
            perfil.sexo = int(sexo)

        else:
            if not flag: messages.add_message(request, messages.WARNING, 'Por Favor preencha todos os campos')            
        if request.FILES:
            perfil.foto = request.FILES["foto"]
        else: #Se não tiver sido enviada uma foto padrão eh salva no lugar
            if not flag:
                media_root = settings.MEDIA_ROOT
                media_root = os.path.join(media_root, "images", "user")                
                file_name = "{}.png".format(username)
                path = os.path.join(media_root, file_name)               
                urllib.request.urlretrieve('https://n8d.at/wp-content/plugins/aioseop-pro-2.4.11.1/images/default-user-image.png', path)
                perfil.foto="images/user/{}".format(file_name)

        #Recebe o atributo relacionado ao numero de telefone
        telefone_numero = request.POST.get('telefone', '').strip()
        telefone_numero = telefone_numero.replace('(', '').replace(')','').replace(' ', '').replace('-', '')

        #Verifica se o atributo é vazio, se for o telefone não é criado
        if telefone_numero:
            #Cria a entidade telefone
            telefone = Telefone()
            telefone.numero = telefone_numero
            tentativa_de_cadastro['telefone'] = telefone_numero          
            #Salva o telefone criado
            if not flag:
                telefone.save()
                #Associa o telefone ao perfil
                perfil.telefone = telefone
        if not flag:
            #Recebe os atributos relacionados ao endereço
            cep = request.POST.get('cep', '').strip()
            rua = request.POST.get('rua', '').strip()
            numero = request.POST.get('numero', '').strip()
            bairro = request.POST.get('bairro', '').strip()
            cidade = request.POST.get('cidade', '').strip()
            estado = request.POST.get('estado', '').strip()

            #Verifica se algum dos atributos é vazio, se for o endereço não é criado
            if cep and rua and numero and bairro and cidade and estado and not flag:
                #Cria a entidade endereço
                endereco = Endereco()
                endereco.cep = cep
                endereco.rua = rua
                endereco.numero = numero
                endereco.bairro = bairro
                endereco.cidade = cidade
                endereco.estado = estado
                #Salva o endereço criado
                endereco.save()
                #Associa o endereco ao perfil
                perfil.endereco = endereco

            #Caso tudo corra bem, salva as entidades obrigatorias e suas associações
            #Salva a entidade user
            if first_name and last_name and email and username and password:
                #Cria a entidade user
                user = User.objects.create_user(username, email, password)
                user.first_name = first_name
                user.last_name = last_name

            else:
                if not flag: messages.add_message(request, messages.WARNING, 'Por Favor preencha todos os campos')
            user.save()
            #Associa o user ao perfil
            perfil.user = user
            #Salva o perfil
            perfil.save()
            #Recebe o atributo relacionado ao gênero
            tipo = request.POST.get('genero', False).strip()

            #Verifica se o atributo é vazio, se for o gênero não é criado
            if tipo:
                #Cria a entidade gênero
                genero = GeneroLivro()
                genero.perfil = perfil
                genero.tipo = tipo
                #Salva o genero criado
                genero.save()
            login(request, user)
            request.session["perfil"] = Perfil.objects.get(user=user).id
            next = request.GET.get("next", '')
            if next:
                return HttpResponse((next))
            else: 
                return HttpResponse(reverse("home:index"))
    
    if flag:
        tentativa_de_cadastro['flag'] = True
        request.session["tentativa_de_cadastro"] = tentativa_de_cadastro
        url = reverse('accounts:login') 
        next = request.GET.get("next", '')
        if next:
                url += '?next={}'.format(next)
        return HttpResponse(url)
    return HttpResponse(reverse('home:index'))

def loginscreen(request):
    if ('perfil' in request.session):
        return redirect(reverse('home:index'))
    next = request.GET.get("next", "")
    tentativa_de_cadastro = request.session.pop("tentativa_de_cadastro", {
        'nome':'',
        'sobrenome': '',
        'usuario': '',
        'email':'',
        'telefone':'',
        'flag': False
    })
    context={
        "next": next,
        "tentativa": tentativa_de_cadastro        
        }
    return render(request, 'registration/login.html', context=context)


@login_required
def Editar(request):
    perfil = Perfil.objects.get(id=request.session['perfil'])
    cep = request.POST.get('cep', perfil.endereco.cep)
    if cep != perfil.endereco.cep:
        perfil.endereco.cep = cep
        rua = request.POST.get('rua', '')
        bairro =  request.POST.get('bairro', '')
        cidade =  request.POST.get('cidade', '')
        estado =  request.POST.get('estado', '')
        if rua:
            perfil.endereco.rua = rua
            perfil.endereco.bairro = bairro
            perfil.endereco.cidade = cidade
            perfil.endereco.estado = estado
        perfil.endereco.save()
            
    elif cep:
        perfil.endereco.numero = request.POST.get('numero', '')
        perfil.endereco.save()
    
    telefone = request.POST.get('telefone', perfil.telefone.numero)
    telefone = telefone.replace('(', '').replace(')','').replace(' ', '').replace('-', '')
    
    perfil.telefone.numero = telefone
    perfil.telefone.save()
    FavGenero = request.POST['genero']
    FavGeneroUser = perfil.generolivro_set.all()[0]
    FavGeneroUser.tipo = int(FavGenero)
    FavGeneroUser.save()
    perfil.save()
    novasenha = request.POST.get('senha', '')
    if novasenha:
        del request.session['perfil']
        perfil.user.set_password(novasenha)
        perfil.user.save()
        messages.add_message(request, messages.INFO, 'Por favor, entre novamente com a nova senha')        
        logout(request)
        return redirect(reverse('accounts:login'))
    
    messages.add_message(request, messages.SUCCESS, 'Dados alterados com sucesso')
    return redirect(reverse('accounts:visualizar', args=(perfil.user.username,)))
@login_required
def loginAdmin(request):
    return redirect("/admin")


def AddPerfilContext(request):
    """ 
    Esse método é um processador de contexto
    ele serve para adicionar o contexto perfil(o usuário atual logado) em todos os templates automaticamente
    """
    context = {}
    if 'perfil' in request.session:
        p = Perfil.objects.get(user=request.user)
        context['perfil'] = p

    return context

def Visualizar(request, username):
    context = {}
    # Caso o usuário da url e o que está logado seja o mesmo, visualiza o perfil
    if username.lower() == request.user.username.lower():   
        context['perfil'] = Perfil.objects.get(id=request.session['perfil'])
        return render(request, 'registration/visualizar_perfil.html', context=context)
    # Caso contrário, o usuário logado visualiza o acervo so usuário da url
    else:                             
        User = get_object_or_404(Perfil, user__username__iexact=username)
        context['livros_user'] = LivroUsuario.objects.filter(perfil=User)
        context['userview'] = Perfil.objects.get(user__username=username)
        return render(request, 'registration/visualizar_acervo.html', context=context)



def paginaAcervo(request):  # Retorna para o template da pagina do acervo todos os livros do sistema e do usuario
    context = {}
    context['livros_bibmap'] = Livro.objects.all()
    context['livros_user'] = LivroUsuario.objects.filter(perfil=request.session['perfil']).order_by('livro')
    context['userview'] = Perfil.objects.get(user=request.user)

    return(render(request, 'registration/visualizar_acervo.html', context=context))
    
@login_required
def adicionarLivro(request):
    if request.user.id == request.session['perfil']:
        perfil = Perfil.objects.get(id=request.session['perfil'])
        livro = Livro.objects.get(pk=request.POST['livros_id'])
        estado = request.POST['estado']
        livro_usuario = LivroUsuario()
        livro_usuario.perfil = perfil
        livro_usuario.livro = livro
        livro_usuario.estado = estado
        livro_usuario.save()
        
        messages.add_message(
           request,
           messages.SUCCESS,
           'Livro adicionado com sucesso!'
        )
    else:
        messages.add_message(
        request,
        messages.ERROR,
        'Você não tem autorização para fazer isso.'
        )

    return HttpResponseRedirect(reverse('accounts:paginaAcervo'))

@login_required
def excluirLivro(request, livro_usuario_id): 
    if request.user.id == request.session['perfil']:
        livro_usuario = LivroUsuario.objects.get(pk=livro_usuario_id)
        livro_usuario.delete()

        messages.add_message(
            request,
            messages.SUCCESS,
            'Livro excluído com sucesso!'
        )
    else:
        messages.add_message(
            request,
            messages.ERROR,
            'Você não tem autorização para excluir este livro.'
        )
    
    return HttpResponseRedirect(reverse('accounts:paginaAcervo'))

@login_required
def SelecionaTrocaDeLivro(request, livrosolicitado_id):
    #Recupera o livro solicitado para troca
    livro_solicitado = LivroUsuario.objects.get(pk=livrosolicitado_id)

    context = {
        'livro_solicitado': livro_solicitado,
    }

    return render(request, 'accounts/selecionatrocadelivro.html', context)


@login_required
def SolicitaTrocaDeLivro(request, livrousuario_id, livrosolicitado_id):
    #Recebe o livro escolhido pelo usuário, para troca
    livro_solicitante = LivroUsuario.objects.get(pk = livrousuario_id)
    #Recebe o livro que o usuário deseja receber na troca
    livro_solicitado = LivroUsuario.objects.get(pk = livrosolicitado_id)

    #Cria o objeto que vai armazenar os livros solicitados
    trocalivro = TrocaLivro()
    trocalivro.livro_solicitante = livro_solicitante
    trocalivro.livro_solicitado = livro_solicitado
    trocalivro.save()

    messages.add_message(request, messages.SUCCESS, "Solicitação de troca enviada")
    
    return redirect(reverse('accounts:TrocasDeLivros'))

@login_required
def TrocasDeLivros(request):
    #Query que gera uma lista com todas as trocas em que o usuário logado participou como solicitante ou solicitado
    #lista_de_trocas = TrocaLivro.objects.filter(livro_solicitante__perfil__user_id = request.user.id | livro_solicitado__perfil__user_id = request.user.id)
    #lista_de_trocas = TrocaLivro.objects.filter(TrocaLivro(livro_solicitante__perfil__user_id = request.user.id) | TrocaLivro(livro_solicitado__perfil__user_id = request.user.id))
    lista_de_trocas = TrocaLivro.objects.filter(livro_solicitante__perfil__user_id = request.user.id) | TrocaLivro.objects.filter(livro_solicitado__perfil__user_id = request.user.id)

    context = {
        'lista_de_trocas': lista_de_trocas,
    }

    return render(request, 'accounts/trocasdelivros.html', context)


@login_required
def FinalizaTrocaDeLivro(request, trocalivro_id):
    #Recebe a troca
    trocalivro = TrocaLivro.objects.get(pk = trocalivro_id)
    confirmacao = request.POST['confirmacao']
    #Finaliza a troca, como realizada ou cancelada
    if confirmacao:
        trocalivro.confirmacao = True
        #Caso a troca seja confirmada, os livros associados a usuários vão mudar de dono
        usuario_solicitante = trocalivro.livro_solicitante.perfil
        usuario_solicitado = trocalivro.livro_solicitado.perfil
        trocalivro.livro_solicitante.perfil = usuario_solicitado
        trocalivro.livro_solicitante.save()
        trocalivro.livro_solicitado.perfil = usuario_solicitante
        trocalivro.livro_solicitado.save()
        trocalivro.data_finalizacao = datetime.date.today()
        trocalivro.save()
        messages.add_message(request, messages.SUCCESS, "Troca confirmada")

    else:
        trocalivro.confirmacao = False
        trocalivro.data_finalizacao = datetime.date.today()
        trocalivro.save()
        messages.add_message(request, messages.WARNING, "Troca recusada")
       
    trocalivro.data_finalizacao = datetime.datetime.now()

    return redirect(reverse('accounts:TrocasDeLivros'))