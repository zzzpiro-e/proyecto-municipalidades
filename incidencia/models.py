from django.db import models
from departamento.models import Departamento
from territorial.models import Territorial
from encuesta.models import Encuesta


class Incidencia(models.Model):
    STATE_PENDIENTE = 'Pendiente'
    STATE_ACEPTADO = 'Aceptado'
    STATE_RECHAZADO = 'Rechazado'
    STATE_BLOQUEADO = 'Bloqueado'
    STATE_ASIGNADA = 'Asignada'
    STATE_RESUELTO = 'Resuelto'
    STATE_CHOICES = [
       
        (STATE_BLOQUEADO, 'Bloqueado'),
    ]
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
    state=models.CharField(max_length=100,null=True,blank=True,choices=STATE_CHOICES,default=STATE_PENDIENTE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    estado=models.CharField(max_length=100,null=True,blank=True,default='Pendiente')

    state=models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=STATE_CHOICES,
        default=STATE_PENDIENTE
    )
    
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Incidencia'
        verbose_name_plural='Incidencias'
        ordering=["titulo"]

    def __str__(self):
        return self.titulo
    
    

class MultimediaIncidencia(models.Model):
    incidencia = models.ForeignKey(Incidencia, on_delete=models.CASCADE, related_name='multimedia')
    TIPO_CHOICES = [
        ('imagen', 'Imagen'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('otro', 'Otro'),
    ]
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default='imagen')
    path = models.FileField(upload_to='archivos_incidencias/%Y/%m/%d/') 
    created = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Archivo Multimedia'
        verbose_name_plural = 'Archivos Multimedia'
        ordering = ['-created']

    def __str__(self):
        return f"{self.get_tipo_display()} de Incidencia {self.incidencia.id}"