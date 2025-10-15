from django.urls import path
from encuesta import views

encuesta_urlpatterns = [
    path('main_encuesta/', views.main_encuesta, name='main_encuesta'),
    path('bloquear_encuesta/<int:pk>/', views.bloquear_encuesta, name='bloquear_encuesta'),
    path('editar_encuesta/<int:encuesta_id>/', views.editar_encuesta, name='editar_encuesta'),
]
