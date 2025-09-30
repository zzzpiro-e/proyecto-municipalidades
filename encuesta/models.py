from django.db import models
from django.contrib.auth.models import User
from departamento.models import Departamento

class Encuesta(models.Model):
    departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE)
    nombre_encuesta=models.CharField(max_length=200,null=False,blank=False)
    descripcion=models.TextField(null=True, blank=True)
    tipo=models.CharField(max_length=50, null=True,blank=True)
    prioridad=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True,default='Activo')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Encuesta'
        verbose_name_plural='Encuestas'
        ordering=["nombre_encuesta"]

    def __str__(self):
        return self.nombre_encuesta