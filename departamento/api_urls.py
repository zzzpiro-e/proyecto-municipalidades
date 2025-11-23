# departamento/api_urls.py (Nuevo archivo)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import DepartamentoViewSet

router = DefaultRouter()
# El endpoint será /departamento/api/departamentos/
router.register(r'departamentos', DepartamentoViewSet) 

urlpatterns = [
    path('', include(router.urls)), 
]