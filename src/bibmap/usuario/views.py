from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from biblioteca.models import Endereco
from accounts.models import LivroUsuario
from .models import Perfil, Telefone, GeneroLivro
from django.http import HttpResponse
import urllib.request
import logging
import datetime
from django.utils import timezone
from django.conf import settings
import os
from django.contrib import messages
from PIL import Image

logger = logging.getLogger(__name__)

# Create your views here.

def AlterarFoto(request, perfil_id):
    print('-----\n', request.FILES['foto'])
    perfil = Perfil.objects.get(id=perfil_id)
    if perfil.foto:
        perfil.foto.delete()
    foto = request.FILES['foto']
    perfil.foto = foto
    perfil.save()
    ret = {'success': True,
           'newUrl': perfil.foto.url
           }
    return HttpResponse(ret)

#View responsável por listar todos os usuários cadastrados
@login_required
def ListarUsuarios(request):
    
    perfil = Perfil.objects.get(id=request.session["perfil"])
    if perfil.grupo != 2:
        return render(request, "registration/unauthorized.html")
    #Query para recuperar todos os usuários e armazenar em uma lista
    lista_usuarios = Perfil.objects.all()
    context = {
        'lista_usuarios': lista_usuarios,
    }

    context["perfil"] = perfil
    
    return render(request, 'usuario/usuario_listar.html', context)

#View responsável por salvar um usuário
@login_required
def SalvarCadastroUsuario(request):
    perfil = Perfil.objects.get(id=request.session["perfil"])
    if perfil.grupo != 2:
        return render(request, "registration/unauthorized.html")
    #Verifica se já existe uma conta de user com o username passado no formulário
    verifica_username = User.objects.filter(username = request.POST['username'].strip()).exists()
    verifica_email = User.objects.filter(email = request.POST['email'].strip())

    #Se existir o context ira repassar uma mensagem de erro e impedir a tentativa de criar um user com username já cadastrado
    if verifica_username or verifica_email:
        messages.add_message(request, messages.ERROR, 'Usuário já existente')
        return HttpResponse(reverse('usuario:ListarUsuarios'))
        return redirect(reverse('usuario:ListarUsuarios'))

    #Se não existir um novo user será criado
    else:
        #Recebe as informações mais básicas do usuário, todas obrigatorias
        first_name = request.POST.get('first_name', False).strip()
        last_name = request.POST.get('last_name', False).strip()
        email = request.POST.get('email', False).strip()
        username = request.POST.get('username', False).strip()
        password = request.POST.get('password', False).strip()

        #Se algumas delas estiver em branco, o cadastro será impedido
        if first_name and last_name and email and username and password:
            #Cria a entidade user
            user = User.objects.create_user(username, email = email, password = password, first_name = first_name, last_name = last_name)
            """ user = User()
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.password = password """

        else:
            messages.add_message(request, messages.WARNING, 'Por Favor preencha todos os campos')
            return HttpResponse(reverse('usuario:ListarUsuarios'))
            return redirect(reverse('usuario:ListarUsuarios'))

        #Cria a entidade perfil
        perfil = Perfil()
        #Recebe o atributo sexo, tambem obrigatorio
        sexo = request.POST.get('sexo', False)

        #Se estiver em branco o cadastro é cancelado
        if sexo:
            #Caso não seja, o mesmo é atribuido a entidade perfil
            perfil.sexo = int(sexo)

        else:
            messages.add_message(request, messages.WARNING, 'Por Favor preencha todos os campos')     
            return HttpResponse(reverse('usuario:ListarUsuarios'))       
            return redirect(reverse('usuario:ListarUsuarios'))

        grupo = request.POST.get('grupo', False)
        if grupo:
            perfil.grupo = grupo
        else:
            messages.add_message(request, messages.ERROR, 'É necessário definir o tipo de usuário')     
            return HttpResponse(reverse('usuario:ListarUsuarios'))       
            return redirect(reverse('usuario:ListarUsuarios'))
        #Caso tenha sido enviada foto, a mesma é salva
        if request.FILES:
            perfil.foto = request.FILES["foto"]
        else: #Se não tiver sido enviada uma foto padrão eh salva no lugar
            media_root = settings.MEDIA_ROOT
            media_root = os.path.join(media_root, "images", "user")                
            file_name = "{}.png".format(username)
            path = os.path.join(media_root, file_name)               
            urllib.request.urlretrieve('https://n8d.at/wp-content/plugins/aioseop-pro-2.4.11.1/images/default-user-image.png', path)
            perfil.foto="images/user/{}".format(file_name)

        #Recebe o atributo relacionado ao numero de telefone
        telefone_numero = request.POST.get('telefone', '').strip()

        #Verifica se o atributo é vazio, se for o telefone não é criado
        if telefone_numero:
            #Cria a entidade telefone
            telefone = Telefone()
            telefone.numero = telefone_numero
            #Salva o telefone criado
            telefone.save()
            #Associa o telefone ao perfil
            perfil.telefone = telefone

        #Recebe os atributos relacionados ao endereço
        cep = request.POST.get('cep', '').strip()
        rua = request.POST.get('rua', '').strip()
        numero = request.POST.get('numero', '').strip()
        bairro = request.POST.get('bairro', '').strip()
        cidade = request.POST.get('cidade', '').strip()
        estado = request.POST.get('estado', '').strip()

        #Verifica se algum dos atributos é vazio, se for o endereço não é criado
        if cep and rua and numero and bairro and cidade and estado:
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
        #user.save()
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
    messages.add_message(request, messages.SUCCESS, 'Usuário cadastrado com sucesso')
    return HttpResponse(reverse('usuario:ListarUsuarios'))

#View responsável por retornar, para visualização, um usuário já cadastrado no sistema
@login_required
def VisualizarUsuario(request, perfil_name):
    perfil = Perfil.objects.get(id=request.session["perfil"])
    if perfil.grupo != 2:
        return render(request, "registration/unauthorized.html")
    perfil = get_object_or_404(Perfil, user__username__iexact = perfil_name)
    
    lista_de_genero = GeneroLivro.objects.filter(perfil = perfil)[0]
    context = {
        'perfilEdit': perfil,
        'lista_de_genero': lista_de_genero,
    }
    context["perfil"] = perfil
    return render(request, 'usuario/visualizar_usuario.html', context)

#View responsável por salvar um usuário
@login_required
def SalvarEditarUsuario(request, perfil_id):
    perfil = Perfil.objects.get(id=request.session["perfil"])
    if perfil.grupo != 2:
        return render(request, "registration/unauthorized.html")
    #Recupera o perfil informado no banco de dados
    perfil = get_object_or_404(Perfil, pk = perfil_id)

    if perfil.user.is_active:
        #Recebe as informações mais básicas do usuário, todas obrigatorias
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if password:
            perfil.user.set_password(password)
        #Se algumas delas estiver em branco, o cadastro será impedido
        if first_name and last_name and email and username:
            #Edita o usuario com as informações passadas no formulário de cadastro
            perfil.user.first_name = first_name
            perfil.user.last_name = last_name
            perfil.user.email = email
            perfil.user.username = username
            perfil.user.save()
        #Caso as obrigatorias estejam vazias, o usuário verá uma mensagem de erro
        else:
            messages.add_message(request, messages.WARNING, 'É necessário preencher todos os campos')      
            return redirect(reverse('usuario:ListarUsuarios'))

        #Recebe o atributo sexo, tambem obrigatorio
        sexo = request.POST.get('sexo', False)

        #Se estiver em branco o cadastro é cancelado
        if sexo:
            #Caso não seja, o mesmo é atribuido a entidade perfil
            perfil.sexo = int(sexo)

        else:
            messages.add_message(request, messages.WARNING, 'É necessário preencher todos os campos')    
            return redirect(reverse('usuario:ListarUsuarios'))

        grupo = request.POST.get('grupo', 0)
        perfil.grupo = grupo
        
        #Caso seja tenha foto, a mesma é salva
        #Recebe o atributo relacionado ao numero de telefone
        telefone_numero = request.POST.get('telefone', '').strip()

        #Verifica se o atributo é vazio, se for o telefone não é atualizado
        if telefone_numero:
            #Recebe o telefone do usuario
            #verifica_telefone = Telefone.objects.filter(pk = perfil.telefone.id)

            #Verifica se o usuário possui um telefone cadastrado
            if perfil.telefone:
                #Caso tenha, o número é atualizado
                perfil.telefone.numero = telefone_numero
                perfil.telefone.save()
            #Caso não tenha, uma nova entidade vai ser criada
            else:
                telefone = Telefone()
                telefone.numero = telefone_numero
                #Salva o telefone criado
                telefone.save()
                #Associa o telefone ao perfil
                perfil.telefone = telefone

        #Recebe os atributos relacionados ao endereço
        cep = request.POST.get('cep', '').strip()
        rua = request.POST.get('rua', '').strip()
        numero = request.POST.get('numero', '').strip()
        bairro = request.POST.get('bairro', '').strip()
        cidade = request.POST.get('cidade', '').strip()
        estado = request.POST.get('estado', '').strip()

        #Verifica se algum dos atributos é vazio, se for o endereço não é atualizado
        if cep and rua and numero and bairro and cidade and estado:
            #Recebe o endereço do usuário
            #verifica_endereco = Endereco.objects.filter(pk = perfil.endereco.id)

            #Verifica se o usuário possui um endereço cadastrado
            if perfil.endereco:
                #Caso tenha, o endereço é atualizado
                perfil.endereco.cep = cep
                perfil.endereco.rua = rua
                perfil.endereco.numero = numero
                perfil.endereco.bairro = bairro
                perfil.endereco.cidade = cidade
                perfil.endereco.estado = estado
                perfil.endereco.save()
            #Caso não tenha, uma nova entidade vai ser criada
            else:
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
        perfil.user.save()
        #Salva o perfil
        perfil.save()

        #if request.FILES:
        #    x = float(request.POST['x'])
        #    y = float(request.POST['y'])
        #    width = float(request.POST['width'])
        #    height = float(request.POST['height'])
        #    # A partir daqui a foto será alterada pra ficar em proporção 1:1
        #    im = Image.open(perfil.foto) # Abrir a foto
        #    im = im.crop((x, y, x+width, y+height))
        #    im.save(perfil.foto.path, quality=100)
        
        #Recebe o atributo relacionado ao genero
        tipo = request.POST.get('genero', 1).strip()

        #Verifica se o atributo é vazio, se for o genero não é atualizado
        if tipo:
            #Recebe o gênero de livro preferido do usuário
            verifica_genero = GeneroLivro.objects.filter(perfil = perfil_id)

            #Verifica se o usuário possui um gênero de livro cadastrado
            if verifica_genero:
                #Caso tenha, o gênero é atualizado
                genero = GeneroLivro.objects.get(perfil = perfil_id)
                genero.tipo = tipo
                genero.save()
            #Caso não tenha, uma nova entidade vai ser criada
            else:
                #Cria a entidade gênero
                genero = GeneroLivro()
                genero.perfil = perfil
                genero.tipo = tipo
                #Salva o genero criado
                genero.save()

    messages.add_message(request, messages.SUCCESS, 'Usuário editado com sucesso')
    return redirect(reverse('usuario:ListarUsuarios'))

#View responsável por alterar o status de um usuário
@login_required
def AlterarStatusUsuario(request, user_id):
    perfil = Perfil.objects.get(id=request.session["perfil"])
    if perfil.grupo != 2:
        return render(request, "registration/unauthorized.html")
    user = get_object_or_404(User, pk = user_id)

    user.is_active = (not user.is_active)
    user.save()

    messages.add_message(request, messages.SUCCESS, 'Status alterado com sucesso')

    return redirect(reverse('usuario:ListarUsuarios'))