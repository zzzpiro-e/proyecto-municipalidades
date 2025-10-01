from django.db import models
from django.contrib.auth.models import User

class Direccion(models.Model):
    usuario=models.OneToOneField(User, on_delete=models.SET_NULL,null=True,blank=True)
    nombre_direccion=models.CharField(max_length=200,null=False,blank=False)
    nombre_encargado=models.CharField(max_length=200,null=False,blank=True)
    correo_encargado=models.EmailField(max_length=254,null=False,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True,default='Activo')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Direccion'
        verbose_name_plural='Direcciones'
        ordering=["nombre_direccion"]

    def __str__(self):
        return self.nombre_direccion

