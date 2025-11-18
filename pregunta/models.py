from django.db import models

class Pregunta(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    autor = models.CharField(max_length=100)
    state = models.CharField(max_length=10, default='Activo')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'

    def __str__(self):
        return self.titulo


class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    contenido = models.TextField()
    autor = models.CharField(max_length=100)
    state = models.CharField(max_length=10, default='Activo')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'

    def __str__(self):
        return f"Respuesta de {self.autor} a '{self.pregunta.titulo}'"