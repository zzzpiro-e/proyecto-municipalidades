from django.urls import path
from territorial import views

territorial_urlpatterns=[
    path('main_territorial/',views.main_territorial, name='main_territorial'),
    path('crear_territorial/',views.crear_territorial, name='crear_territorial'),
    path('guardar_territorial/',views.guardar_territorial, name='guardar_territorial'),
    path('editar_territorial/', views.editar_territorial, name='editar_territorial_post'),
    path('editar_territorial/<int:territorial_id>/', views.editar_territorial, name='editar_territorial'),
    path('ver_territorial/<int:territorial_id>/', views.ver_territorial, name='ver_territorial'),
    path('lista_editar/', views.lista_editar_territorial, name='lista_editar_territorial'),
]