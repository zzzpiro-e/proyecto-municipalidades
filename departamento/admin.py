from django.contrib import admin

# Register your models here.

from .models import Departamento

# Para mostrar en el panel admin y realizar prueba
admin.site.register(Departamento)