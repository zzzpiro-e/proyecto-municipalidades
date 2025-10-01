from django.urls import path
from departamento import views

departamento_urlpatterns=[
     path('main_departamento/',views.main_departamento, name='main_departamento'),
     path('crear_departamento/',views.crear_departamento, name='crear_departamento'),
     path('guardar_departamento/',views.guardar_departamento, name='guardar_departamento'),

]
