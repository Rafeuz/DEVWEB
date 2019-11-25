from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'accounts'
urlpatterns = [
    path("trylogin/", views.trylogin, name="trylogin"),
    path("logout/", views.trylogout, name="trylogout"),
    path("login/", views.loginscreen, name="login"),
    path('createacc/', views.Cadastrar, name="createacc"),
    path('editar/', views.Editar, name="editar"),
    path('editar/changephoto', views.EditarFoto, name="modificar_foto"),
    path('acervo/', views.paginaAcervo, name="paginaAcervo"),
    path('adicionarLivro/', views.adicionarLivro, name="adicionarLivro"),
    path('excluirLivro/<int:livro_usuario_id>', views.excluirLivro, name="excluirLivro"),
    path('selecionatrocadelivro/<int:livrosolicitado_id>/', views.SelecionaTrocaDeLivro, name = 'SelecionaTrocaDeLivro'),
    path('solicitatrocadelivro/<int:livrousuario_id>/<int:livrosolicitado_id>/', views.SolicitaTrocaDeLivro, name = 'SolicitaTrocaDeLivro'),
    path('trocasdelivros/', views.TrocasDeLivros, name = 'TrocasDeLivros'),
    path('finalizatrocadelivro/<int:trocalivro_id>/', views.FinalizaTrocaDeLivro, name = 'FinalizaTrocaDeLivro'),
    path('<slug:username>/', views.Visualizar, name='visualizar'), #ESSE SEMPRE TEM QUE FICAR EM ULTIMO
]