from django.urls import path
from . import views

app_name = 'biblioteca'
urlpatterns = [
    path((''), views.Listar, name="listar"),
    path(('status/<int:bibid>/'), views.MudarStatus, name="MudarStatus"),
    path(('adicionar/'), views.Adicionar, name="Adicionar"),
    path(('<int:bibid>/'), views.ListarSingle, name="ListarSingle"),
    path(("Editar/<int:bibid>/"), views.Editar, name="Editar"),
    path('<int:biblioteca_id>/AssociarLivroBiblioteca/', views.AssociarLivroBiblioteca, name = "AssociarLivroBiblioteca"),
    path('<int:livroassociado_id>/EditarLivroAssociado/', views.EditarLivroAssociado, name = "EditarLivroAssociado"),
    path('<int:livroassociado_id>/EditarStatusLivroAssociado/', views.EditarStatusLivroAssociado, name = "EditarStatusLivroAssociado"),
] 
