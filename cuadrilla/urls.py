from django.urls import path
from cuadrilla import views

cuadrilla_urlpatterns=[
    path('main_cuadrilla/',views.main_cuadrilla, name='main_cuadrilla'),
    path('crear_cuadrilla/',views.crear_cuadrilla, name='crear_cuadrilla'),
    path('guardar_cuadrilla/',views.guardar_cuadrilla, name='guardar_cuadrilla'),
]