from django.db import models
from django.contrib.auth.models import User
from departamento.models import Departamento
from incidencia.models import Incidencia

class Cuadrilla(models.Model):
    usuario=models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_cuadrilla=models.CharField(max_length=250,null=False,blank=False)
    tipo=models.CharField(max_length=100,null=False,blank=True)
    departamento=models.ForeignKey(Departamento,on_delete=models.CASCADE)
    state=models.CharField(max_length=100,null=True,blank=True,default='Activo')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Cuadrilla'
        verbose_name_plural='Cuadrillas'
        ordering=["nombre_cuadrilla"]

    def __str__(self):
        return self.nombre_cuadrilla

class Registro_trabajo(models.Model):
    incidencia=models.ForeignKey(Incidencia, on_delete=models.CASCADE, related_name='incidencias')
    cuadrilla=models.ForeignKey(Cuadrilla,on_delete=models.CASCADE, related_name='cuadrillas')
    fecha=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    descripcion=models.TextField(null=True,blank=True)
    estado=models.CharField(max_length=100,null=True,blank=True,default='')

    class Meta:
        verbose_name='Registro'
        verbose_name_plural='Registros'
        ordering=["incidencia"]

    def __str__(self):
        return f"Trabajo de {self.cuadrilla} en {self.incidencia}"
