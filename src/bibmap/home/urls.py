from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.listarLivrosBibliotecas, name="index"),
    path('livros/<int:livro_id>', views.visualizarLivro, name="visualizarLivro"),
    path('bibliotecas/<int:biblioteca_id>', views.visualizarBiblioteca, name="visualizarBiblioteca"),
    path('livros/', views.listarLivros, name="listarLivros"),
    path('bibliotecas/', views.listarBibliotecas, name="listarBibliotecas"),
    path('search/', views.PaginaPesquisa, name="PaginaPesquisa"),
    path('search/<int:page>', views.Pesquisa, name="Pesquisar")
]