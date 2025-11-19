from django.db import models
from encuesta.models import Encuesta
from incidencia.models import Incidencia

class Pregunta(models.Model):
    encuesta=models.ForeignKey(Encuesta,on_delete=models.CASCADE,null=True,blank=True,related_name='preguntas')
    titulo = models.CharField(max_length=255)
    

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'

    def __str__(self):
        return self.titulo


class Respuesta(models.Model):
    incidencia=models.ForeignKey(Incidencia,on_delete=models.CASCADE,null=True,blank=True)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    contenido = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'

    def __str__(self):
        return self.contenido