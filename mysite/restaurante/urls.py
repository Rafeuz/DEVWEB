from django.urls import path
from . import views

app_name = 'restaurante'
urlpatterns = [
    path('', views.index, name='index'),
    path('adicionar/', views.adicionar, name='adicionar')
]