from django.contrib import admin
from django.urls import path
from .views import GerarToken, ValidarToken

urlpatterns = [
    path('gerar/', GerarToken.as_view(), name='gerar_token'),
    path('validar/', ValidarToken.as_view(), name='validar_token'),
    path('admin/', admin.site.urls)
]