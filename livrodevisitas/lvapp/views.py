from django.shortcuts import render
from .models import Mensagens
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

# Create your views here.
def index(request):
	mensagens = Mensagens.objects.all()
	contexto = {'mensagens': mensagens}
	return render(request, 'lvapp/index.html', contexto)

def enviar(request):
	mensagens = Mensagens(nome=request.POST['nome'], texto=request.POST['texto'])
	mensagens.save()
	return HttpResponseRedirect(reverse('lvapp:index'))

