from django.urls import path
from incidencia import views

incidencia_urlpatterns=[
     path('gestion_incidencia/',views.gestion_incidencia, name='gestion_incidencia'),
     path('crear_incidencia/',views.crear_incidencia, name='crear_incidencia'),
     path('guardar_incidencia/',views.guardar_incidencia, name='guardar_incidencia'),
     path('editar_incidencia/', views.editar_incidencia, name='editar_incidencia_post'),
     path('editar_incidencia/<int:incidencia_id>/', views.editar_incidencia, name='editar_incidencia'),
     path('incidencias_usuario_departamento/', views.incidencias_usuario_departamento, name='incidencias_usuario_departamento'),
     path('bloquear_incidencia/<int:pk>/', views.bloquear_incidencia, name='bloquear_incidencia'),
     path('ver_incidencias_bloqueo/',views.ver_incidencias_bloqueo, name='ver_incidencias_bloqueo'),
     path('ver_incidencia/<int:incidencia_id>/', views.ver_incidencia, name='ver_incidencia'),
     path('aceptar_incidenci/<int:pk>/', views.aceptar_incidencia, name='aceptar_incidencia'),
     path('rechazar_incidenci/<int:pk>/', views.rechazar_incidencia, name='rechazar_incidencia'),
     path('gestion_incidencia_admin/', views.gestion_incidencia_admin, name='gestion_incidencia_admin'),
]