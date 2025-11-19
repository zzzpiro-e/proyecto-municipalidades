from django.urls import path
from multimedia import views

multimedia_urlpatterns = [
    path('subir/', views.subir_archivo, name='subir_archivo'),
]
