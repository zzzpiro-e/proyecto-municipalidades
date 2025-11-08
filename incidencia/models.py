from django.db import models
from departamento.models import Departamento
from territorial.models import Territorial
from encuesta.models import Encuesta



class Incidencia(models.Model):
    departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE)
    territorial=models.ForeignKey(Territorial, on_delete=models.CASCADE)
    titulo=models.CharField(max_length=200,null=False,blank=True)
    tipo=models.CharField(max_length=254,null=False,blank=True)
    ubicacion=models.CharField(max_length=250,null=True,blank=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    nombre_vecino=models.CharField(max_length=250,null=True,blank=True)
    telefono_vecino=models.CharField(max_length=15,null=True,blank=True)
    correo_vecino=models.EmailField(max_length=254,null=True,blank=True)
    encuesta=models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    state=models.CharField(max_length=100,null=True,blank=True,default='Activo')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Incidencia'
        verbose_name_plural='Incidencias'
        ordering=["titulo"]

    def __str__(self):
        return self.titulo
    
