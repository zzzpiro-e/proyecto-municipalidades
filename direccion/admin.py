from django.contrib import admin

# Register your models here.

from .models import Direccion

# Para mostrar en el panel admin y realizar prueba
admin.site.register(Direccion)