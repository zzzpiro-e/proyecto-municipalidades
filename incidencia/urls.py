from django.urls import path
from incidencia import views

incidencia_urlpatterns=[
     path('main_incidencia/',views.main_incidencia, name='main_incidencia')
]