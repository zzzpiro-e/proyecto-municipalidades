# departamento/api_views.py (Código final)
from rest_framework import viewsets
from .models import Departamento
from .serializers import DepartamentoSerializer
from django.contrib.auth.models import User
from direccion.models import Direccion


from rest_framework.decorators import action
from rest_framework.response import Response

class DepartamentoViewSet(viewsets.ModelViewSet):
    """API que permite Listar, Crear, Editar y Eliminar Departamentos."""
    
    queryset = Departamento.objects.select_related('usuario', 'direccion').all()
    serializer_class = DepartamentoSerializer
    
    @action(detail=False, methods=['get'])
    def opciones_form(self, request):
        direcciones = Direccion.objects.all().values('id', 'nombre') 
   
        try:
            usuarios_disponibles = User.objects.filter(
                profile__group__id=3,
                departamento__isnull=True 
            ).values('id', 'username')
        except:
            usuarios_disponibles = User.objects.filter(
                departamento__isnull=True
            ).values('id', 'username')

        return Response({
            'direcciones': list(direcciones),
            'usuarios': list(usuarios_disponibles)
        })