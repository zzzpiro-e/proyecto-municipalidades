from django.urls import path
from territorial import views

territorial_urlpatterns=[
    path('main_territorial/',views.main_territorial, name='main_territorial'),
    path('editar_territorial/', views.editar_territorial, name='editar_territorial_post'),
    path('editar_territorial/<int:territorial_id>/', views.editar_territorial, name='editar_territorial'),
]