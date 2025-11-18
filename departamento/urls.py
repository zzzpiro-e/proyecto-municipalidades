from django.urls import path
from departamento import views

departamento_urlpatterns=[
    path('main_departamento/',views.main_departamento, name='main_departamento'),
    path('gestion_departamento/',views.gestion_departamento, name='gestion_departamento'),
    path('crear_departamento/',views.crear_departamento, name='crear_departamento'),
    path('guardar_departamento/',views.guardar_departamento, name='guardar_departamento'),
    path('editar_departamento/', views.editar_departamento, name='editar_departamento_post'),
    path('editar_departamento/<int:departamento_id>/', views.editar_departamento, name='editar_departamento'),
    path('bloquear_departamento/<int:pk>/', views.bloquear_departamento, name='bloquear_departamento'),
    path('ver_departamento/<int:departamento_id>/', views.ver_departamento, name='ver_departamento'),
    path('ver_departamento_bloqueo/', views.ver_departamento_bloqueo, name='ver_departamento_bloqueo'),
]
    