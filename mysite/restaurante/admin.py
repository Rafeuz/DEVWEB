from django.contrib import admin
from .models import Produto, Comanda, ItemComanda
# Register your models here.
admin.site.register(Produto)
admin.site.register(Comanda)
admin.site.register(ItemComanda)