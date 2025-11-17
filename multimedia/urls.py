from django.urls import path
from . import views

multimedia_url_patterns = [
    path('subir/<int:registro_id>/', views.subir_archivo, name='subir_archivo'), 
]
