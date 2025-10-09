from django.urls import path
from incidencia import views

incidencia_urlpatterns=[
     path('main_incidencia/',views.main_incidencia, name='main_incidencia'),
     path('editar_incidencia/', views.editar_incidencia, name='editar_incidencia_post'),
     path('editar_incidencia/<int:incidencia_id>/', views.editar_incidencia, name='editar_incidencia'),
]