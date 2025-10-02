from django.urls import path
from usuario import views

usuario_urlpatterns=[
    path('main_usuario/',views.main_usuario, name='main_usuario'),
    path('crear_usuario/',views.crear_usuario, name='crear_usuario'),
    path('guardar_usuario/',views.guardar_usuario, name='guardar_usuario'),
]