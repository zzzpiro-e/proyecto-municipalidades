from django.urls import path
from incidencia import views

incidencia_urlpatterns = [
    path('main_incidencia/', views.main_incidencia, name='main_incidencia'),
    path('bloquear_incidencia/<int:pk>/', views.bloquear_incidencia, name='bloquear_incidencia'),
]
