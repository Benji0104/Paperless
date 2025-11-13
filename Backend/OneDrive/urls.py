from django.urls import path
from .Views import autenticacion, funciones

urlpatterns = [
    path('login', autenticacion.google_login, name='login'),
    path('registro', autenticacion.register_google, name='registro'),
    path('callback', autenticacion.google_callback, name='callback'),
    path('perfil', autenticacion.perfil, name='perfil'),
    path('archivos', funciones.listar_archivos, name='archivos'),
    path('descarga/<str:file_id>', funciones.leer_archivo_contenido, name='descarga')
    
]