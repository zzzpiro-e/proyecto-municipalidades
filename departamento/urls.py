from django.urls import path
from departamento import views

departamento_urlpatterns=[
     path('main_departamento/',views.main_departamento, name='main_departamento')
]