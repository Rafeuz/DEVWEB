from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import Postagem, Comentario
from django.utils import timezone

# Create your views here.

def index(request):

	ultimas_postagens = Postagem.objects.filter(data__lte = timezone.now()).order_by('-data')[:20]
	contexto = { 'ultimas_postagens':ultimas_postagens}

	return render(request, 'blog/index.html', contexto)

def detalhes(request, postagem_id):

	postagem = get_object_or_404(Postagem, pk=postagem_id)
	comentarios = Comentario.objects.filter(postagem=postagem_id)
	contexto = { 'postagem':postagem, 'comentarios':comentarios }

	return render(request, 'blog/detalhes.html', contexto)

def salvarcomentarios(request, postagem_id):
	autorpost = request.POST['autor']
	textopost = request.POST['texto']
	comentario = Comentario(autor=autorpost, texto=textopost, postagem=postagem_id)
	comentario.save()
	return HttpResponseRedirect(reverse('blog:detalhes', args=(postagem_id)))