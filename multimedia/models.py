from django.db import models
from incidencia.models import Incidencia

class ArchivoMultimedia(models.Model):
    TIPOS = [
        ('imagen', 'Imagen'),
        ('video', 'Video'),
        ('documento', 'Documento'),
        ('audio', 'Audio'),
    ]

    registro_trabajo = models.ForeignKey(
        Incidencia, 
        on_delete=models.CASCADE,
        related_name='multimedia_archivos'
    )

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    archivo = models.FileField(upload_to='uploads/%Y/%m/%d/')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Archivo Multimedia'
        verbose_name_plural = 'Archivos Multimedia'
        ordering = ['-creado']

    def __str__(self):
        return f"{self.titulo} ({self.tipo})"


