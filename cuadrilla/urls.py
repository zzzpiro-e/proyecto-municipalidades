from django.urls import path
from cuadrilla import views

cuadrilla_urlpatterns=[
    path('main_cuadrilla/',views.main_cuadrilla, name='main_cuadrilla'),
    path('gestion_cuadrilla/',views.gestion_cuadrilla, name='gestion_cuadrilla'),
    path('crear_cuadrilla/',views.crear_cuadrilla, name='crear_cuadrilla'),
    path('guardar_cuadrilla/',views.guardar_cuadrilla, name='guardar_cuadrilla'),
    path('editar_cuadrilla/', views.editar_cuadrilla, name='editar_cuadrilla_post'),
    path('editar_cuadrilla/<int:cuadrilla_id>/', views.editar_cuadrilla, name='editar_cuadrilla'),
    path('ver_cuadrilla/<int:cuadrilla_id>/', views.ver_cuadrilla, name='ver_cuadrilla'),
    path('ver_registro/', views.ver_registro, name='ver_registro'),
    path('bloquear_cuadrilla/<int:pk>/', views.bloquear_cuadrilla, name='bloquear_cuadrilla'),
    path('crear_registro/',views.crear_registro, name='crear_registro'),
    path('ver_incidencias_cuadrilla/', views.ver_incidencias_cuadrilla, name='ver_incidencias_cuadrilla'),
    
]