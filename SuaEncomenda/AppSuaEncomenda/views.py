from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView,UpdateView, DeleteView
from django.urls import reverse
from django.contrib import messages
from .models import Encomenda


def index(request):
    encomendas = Encomenda.objects.all()
    return render(request, 'AppSuaEncomenda/index.html', {'encomendas':encomendas})


class ListarEncomenda(ListView):
	model = Encomenda
	template_name = 'AppSuaEncomenda/index.html'
	context_object_name = 'encomendas'

class DetalheEncomenda(DetailView):
	model = Encomenda

class PostarEncomenda(LoginRequiredMixin, CreateView):
	model = Encomenda
	fields = ['nome', 'descricao', 'preco']

	def form_valid(self, form):
		form.instance.confeiteira = self.request.user
		return super().form_valid(form)

class AtualizarEncomenda(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Encomenda
	fields = ['nome', 'descricao', 'preco']

	def form_valid(self, form):
		form.instance.confeiteira = self.request.user
		return super().form_valid(form)

	def test_func(self):
		encomenda = self.get_object()
		if self.request.user == encomenda.confeiteira:
			return True
		return False	

class ExcluirEncomenda(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Encomenda
	success_url = '/'

	def test_func(self):
		encomenda = self.get_object()
		if self.request.user == encomenda.confeiteira:
			return True
		return False