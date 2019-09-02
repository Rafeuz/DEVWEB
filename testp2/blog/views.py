from django.shortcuts import render
from django.views import generic
from .models import Postagem

# Create your views here.

class IndexView(generic.ListView):
	template = 'blog/index.html'
	contexto = 'postagem'
	def get_queryset(self):
		return Postagem.objects.order_by('data')[:29]

