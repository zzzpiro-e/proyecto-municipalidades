from django.urls import path
from cuadrilla import views

cuadrilla_urlpatterns=[
    path('main_cuadrilla/',views.main_cuadrilla, name='main_cuadrilla'),
    path('crear_cuadrilla/',views.crear_cuadrilla, name='crear_cuadrilla'),
    path('guardar_cuadrilla/',views.guardar_cuadrilla, name='guardar_cuadrilla'),
    path('editar_cuadrilla/', views.editar_cuadrilla, name='editar_cuadrilla_post'),
    path('editar_cuadrilla/<int:cuadrilla_id>/', views.editar_cuadrilla, name='editar_cuadrilla'),
    path('ver/', views.ver_cuadrilla, name='ver_cuadrilla'),
    path('lista_editar/', views.lista_editar_cuadrilla, name='lista_editar_cuadrilla'),
]