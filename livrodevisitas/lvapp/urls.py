from django.urls import path
from . import views

app_name = 'lvapp'
urlpatterns = [
	path('', views.index, name='index'),
    path('enviar', views.enviar, name='enviar'),
]
