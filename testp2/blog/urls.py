from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
	path('', views.index, name='index'),
    path('<int:postagem_id>/', views.detalhes, name='detalhes'),
    path('<int:postagem_id>/salvarcomentarios', views.salvarcomentarios, name='salvarcomentarios'),

]
