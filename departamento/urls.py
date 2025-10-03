from django.urls import path
from departamento import views

departamento_urlpatterns=[
    path('main_departamento/',views.main_departamento, name='main_departamento'),
    path('crear_departamento/',views.crear_departamento, name='crear_departamento'),
    path('guardar_departamento/',views.guardar_departamento, name='guardar_departamento'),
    path('editar_departamento/', views.editar_departamento, name='editar_departamento_post'),
    path('editar_departamento/<int:departamento_id>/', views.editar_departamento, name='editar_departamento'),
    path('lista_editar_departamento/', views.lista_editar_departamento, name='lista_editar_departamento'),
    path('ver_departamento/', views.ver_departamento, name='ver_departamento'),
]
    