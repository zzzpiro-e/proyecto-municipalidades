from django.urls import path
from direccion import views

direccion_urlpatterns = [
    path('ver_direccion/<int:direccion_id>/', views.ver_direccion, name='ver_direccion'),
    path('crear_direccion/', views.crear_direccion, name='crear_direccion'),
    path('guardar_direccion/', views.guardar_direccion, name='guardar_direccion'),
    path('editar_direccion/', views.editar_direccion, name='editar_direccion_post'),
    path('editar_direccion/<int:direccion_id>/', views.editar_direccion, name='editar_direccion'),
    path('bloquear_direccion/<int:pk>/', views.bloquear_direccion, name='bloquear_direccion'),
    path('main_direccion/', views.main_direccion, name='main_direccion'),
]
