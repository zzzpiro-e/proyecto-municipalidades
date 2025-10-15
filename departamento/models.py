from django.db import models
from django.contrib.auth.models import User
from direccion.models import Direccion

class Departamento(models.Model):
    usuario=models.OneToOneField(User, on_delete=models.SET_NULL, null=True,blank=True)
    direccion=models.ForeignKey(Direccion, on_delete=models.CASCADE)
    nombre_departamento=models.CharField(max_length=200,null=False,blank=False)
    activo = models.BooleanField(default=True)  
    state=models.CharField(max_length=100,null=True,blank=True,default='Activo')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Departamento'
        verbose_name_plural='Departamentos'
        ordering=["nombre_departamento"]

    def __str__(self):
        return self.nombre_departamento
