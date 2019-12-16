from django.urls import path, include
from .views import ListarEncomenda, DetalheEncomenda, PostarEncomenda, AtualizarEncomenda, ExcluirEncomenda
from . import views

app_name = 'AppSuaEncomenda'
urlpatterns = [
    path('', ListarEncomenda.as_view(), name='ListarEncomenda'),
    path('encomenda/<int:pk>/', DetalheEncomenda.as_view(), name='DetalheEncomenda'),
    path('encomenda/<int:pk>/atualizar/', AtualizarEncomenda.as_view(), name='AtualizarEncomenda'),
    path('encomenda/<int:pk>/excluir/', ExcluirEncomenda.as_view(), name='ExcluirEncomenda'),
    path('encomenda/nova/', PostarEncomenda.as_view(), name='PostarEncomenda'),
]