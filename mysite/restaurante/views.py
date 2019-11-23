from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Produto, Comanda, ItemComanda

def index(request):
	comandas = Comanda.objects.filter(esta_ativa=True)
	contexto = {'comandas':comandas}
	return render(request, 'restaurante/index.html', contexto)

def adicionar(request, comanda_id, produto_id):
	comanda = get_object_or_404(Comanda, pk=comanda_id)
	produto = get_object_or_404(Produto, pk=produto_id)
	item = ItemComanda(qtd = request.POST['qtd'], comanda=comanda, produto=produto)
	comanda.save()
	return HttpResponseRedirect(reverse('restaurante:index', args=(comanda_id,produto_id,)))

