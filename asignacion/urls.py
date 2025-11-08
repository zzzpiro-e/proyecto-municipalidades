from django.urls import path
from asignacion import views

asignacion_urlpatterns=[
    path("cuadrilla/<int:cuadrilla_id>/asignar_incidencia/", views.asignar_incidencia, name="asignar_incidencia")
]