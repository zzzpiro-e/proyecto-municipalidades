from django.db import models
from django.db import models

class Perfiles(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'perfiles'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=255, unique=True)
    id_perfil = models.ForeignKey(
        Perfiles, on_delete=models.PROTECT,
        db_column='id_perfil', related_name='usuarios'
    )

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
