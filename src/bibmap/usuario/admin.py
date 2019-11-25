from django.contrib import admin
from .models import Telefone, Perfil, GeneroLivro, Operadores
from django.contrib.auth.models import Group, Permission

class PerfilAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print("entrouadmin")
        print(obj.grupo)
        print(obj.user.is_superuser)
        if obj.grupo == 0:
            my_group = Group.objects.get(name='Usuário') 
            #permissoes = Group
            my_group.user_set.add(obj.user)
        elif obj.grupo == 1:
            my_group = Group.objects.get(name='Operador') 
            #permissoes = Group
            my_group.user_set.add(obj.user)
        elif obj.grupo == 2:
            obj.user.is_superuser = True
            obj.user.is_staff = True
            print(obj.user.is_superuser)
            obj.user.save()
        super().save_model(request, obj, form, change)

admin.site.register(Telefone)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(GeneroLivro)
admin.site.register(Operadores)