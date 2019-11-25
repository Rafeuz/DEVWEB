from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Para imagens
from django.conf.urls.static import static # para imagens
from accounts import views
import biblioteca
urlpatterns = [
    path("admin/login/", views.loginAdmin, name="LoginAdmin"),
    path('admin/', admin.site.urls),
    path('gerenciar/biblioteca/', include('biblioteca.urls')),
    path("gerenciar/livro/", include('livro.urls')),
    path("", include('home.urls')),
    path("gerenciar/usuario/", include('usuario.urls')),
    path("accounts/", include('accounts.urls')),
    path(("imagem/<int:bibid>/"), biblioteca.views.testeimagem, name="TesteImagem"),
]

if settings.DEBUG: # para imagens
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
