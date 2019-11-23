from django.shortcuts import render
from .models import Encomenda


def index(request):
    encomendas = Encomenda.objects.all()
    return render(request, 'AppSuaEncomenda/index.html', {encomendas:'encomendas'})