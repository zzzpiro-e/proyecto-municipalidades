from django.db import models
from django.contrib.auth.models import User

class Territorial(models.Model):
    usuario=models.OneToOneField(User, on_delete=models.CASCADE)
    zona_asignada=models.CharField(max_length=250, null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True,default='Activo')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Territorial'
        verbose_name_plural='Territoriales'
        ordering=["usuario__username"]

    def __str__(self):
        return self.usuario.username