from django.urls import path
from direccion import views

direccion_urlpatterns=[
    path('main_direccion/',views.main_direccion, name='main_direccion')
]