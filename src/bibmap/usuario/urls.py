from django.urls import path
from . import views

app_name = 'usuario'
urlpatterns = [
    path('', views.ListarUsuarios, name = 'ListarUsuarios'),
    path('salvar_cadastro_usuario/', views.SalvarCadastroUsuario, name = 'SalvarCadastroUsuario'),
    path('<slug:perfil_name>/', views.VisualizarUsuario, name = 'VisualizarUsuario'),
    path('salvar_edicao_usuario/<int:perfil_id>/', views.SalvarEditarUsuario, name = 'SalvarEditarUsuario'),
    path('alterarfoto/<int:perfil_id>/', views.AlterarFoto, name = 'AlterarFoto'),    
    path('alterar_status_usuario/<int:user_id>/', views.AlterarStatusUsuario, name = 'AlterarStatusUsuario'),
]