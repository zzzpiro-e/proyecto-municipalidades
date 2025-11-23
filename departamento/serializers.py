# departamento/serializers.py (Nuevo archivo)
from rest_framework import serializers
from .models import Departamento

class DepartamentoSerializer(serializers.ModelSerializer):
    # Serializamos las relaciones para que muestren su representación en texto (__str__)
    usuario = serializers.StringRelatedField(read_only=True)
    direccion = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Departamento
        # Campos que expondremos a React, basados en tu models.py
        fields = [
            'id', 
            'nombre_departamento', # Nombre exacto del campo
            'activo', 
            'state', 
            'usuario', 
            'direccion', 
            'created'
        ]