from django.urls import path
from territorial import views

territorial_urlpatterns=[
    path('main_territorial/',views.main_territorial, name='main_territorial'),
   

]