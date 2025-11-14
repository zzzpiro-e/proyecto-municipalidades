from django.shortcuts import render
from django.conf import settings #importa el archivo settings
from django.contrib import messages #habilita la mesajería entre vistas
from django.contrib.auth.decorators import login_required #habilita el decorador que se niega el acceso a una función si no se esta logeado
from django.contrib.auth.models import Group, User # importa los models de usuarios y grupos
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator #permite la paqinación
from django.db.models import Avg, Count, Q #agrega funcionalidades de agregación a nuestros QuerySets
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotFound, HttpResponseRedirect) #Salidas alternativas al flujo de la aplicación se explicará mas adelante
from django.shortcuts import redirect, render #permite renderizar vistas basadas en funciones o redireccionar a otras funciones
from django.template import RequestContext # contexto del sistema
from django.views.decorators.csrf import csrf_exempt #decorador que nos permitira realizar conexiones csrf
from incidencia.models import Incidencia
from registration.models import Profile #importa el modelo profile, el que usaremos para los perfiles de usuarios


# Create your views here.
def home(request):
    return redirect('login')

@login_required
def pre_check_profile(request):
    #por ahora solo esta creada pero aún no la implementaremos
    pass

@login_required
def check_profile(request):  
    try:
        profile = Profile.objects.filter(user_id=request.user.id).get()    
    except:
        messages.add_message(request, messages.INFO, 'Hubo un error con su usuario, por favor contactese con los administradores')              
        return redirect('login')
    if profile.group_id == 1:        
        return redirect('main_admin')
    elif profile.group_id==2:
        return redirect('main_direccion')
    elif profile.group_id==3:
        return redirect('main_departamento')
    elif profile.group_id==4:
        return redirect('main_territorial')
    elif profile.group_id==5:
        return redirect('main_cuadrilla')
    else:
        return redirect('logout')

#funcion temporal
@login_required
def main_admin(request):  
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Hubo un error con su usuario, por favor contactese con los administradores')              
        return redirect('login')

    # Solo admin (group_id = 1)
    if profile.group_id == 1:

        # --- Datos para el dashboard ---
        total_usuarios = User.objects.count()
        total_incidencias = Incidencia.objects.count()
        incidencias_derivadas = Incidencia.objects.filter(estado="Asignada").count()
        incidencias_rechazadas = Incidencia.objects.filter(estado="Rechazada").count()
        incidencias_finalizadas = Incidencia.objects.filter(estado="Resuelto").count()

        context = {
            'total_usuarios': total_usuarios,
            'total_incidencias': total_incidencias,
            'incidencias_derivadas': incidencias_derivadas,
            'incidencias_rechazadas': incidencias_rechazadas,
            'incidencias_finalizadas': incidencias_finalizadas,
        }

        return render(request, 'core/main_admin.html', context)

    else:
        return redirect('logout')

    
    
