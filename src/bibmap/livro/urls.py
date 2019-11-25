from django.urls import path
from . import views

app_name = 'livro'
urlpatterns = [
    path('', views.Listar, name="listar"),
    path('Adicionar', views.Adicionar, name="Adicionar"),
    path('Visualizar/<int:livro_id>', views.ListarSingle, name="ListarSingle"),
    path('Visualizar/<int:livro_id>/<slug:erro>', views.ListarSingle, name="ListarSingleErro"),
    path('<slug:erro>', views.Listar, name="ListarErro"),
    path('Editar/<int:livro_id>', views.Editar, name="Editar"),
    path('Status/<int:livro_id>', views.MudarStatus, name="MudarStatus"),
    
]