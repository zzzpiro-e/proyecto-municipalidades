from django.contrib import admin

# Register your models here.

from .models import Territorial

# Para mostrar en el panel admin y realizar prueba
admin.site.register(Territorial)