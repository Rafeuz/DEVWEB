from django.contrib import admin
from .models import  Biblioteca, Endereco, RecursosOpcionais, LivroAssociado
# Register your models here.
admin.site.register(Biblioteca)

admin.site.register(Endereco)
admin.site.register(RecursosOpcionais)
admin.site.register(LivroAssociado)