from django.db import models
from cuadrilla.models import Cuadrilla
from incidencia.models import Incidencia

class Asignacion(models.Model):
    incidencia=models.ForeignKey(Incidencia, on_delete=models.CASCADE)
    cuadrilla=models.ForeignKey(Cuadrilla,on_delete=models.CASCADE)
    fecha_asignacion=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='Asignacion'
        verbose_name_plural='Asignaciones'
        ordering=["fecha_asignacion"]
