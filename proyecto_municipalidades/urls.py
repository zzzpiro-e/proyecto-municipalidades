"""
URL configuration for proyecto_municipalidades project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from core.urls import core_urlpatterns
from direccion.urls import direccion_urlpatterns
from departamento.urls import departamento_urlpatterns
from territorial.urls import territorial_urlpatterns
from incidencia.urls import incidencia_urlpatterns

urlpatterns = [
    path("",include(core_urlpatterns)),
    path("admin/", admin.site.urls),
    path("direccion/",include(direccion_urlpatterns)),
    path("departamento/",include(departamento_urlpatterns)),
    path("territorial/",include(territorial_urlpatterns)),
    path("usuario/",include('usuario.urls')),
    path("incidencia/",include(incidencia_urlpatterns)),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/',include('registration.urls')),
]
