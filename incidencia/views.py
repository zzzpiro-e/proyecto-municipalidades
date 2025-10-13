from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from registration.models import Profile
from .models import Incidencia
from departamento.models import Departamento
from territorial.models import Territorial
from encuesta.models import Encuesta

@login_required
def main_incidencia(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')
    if profile.group_id in [1, 2, 3, 4, 5]:
        incidencias = Incidencia.objects.filter(state='Activo')
        context = {
            'incidencias': incidencias,
            'profile': profile
        }
        return render(request, 'incidencia/main_incidencia.html', context)
    else:
        return redirect('logout')
    
@login_required
def editar_incidencia(request, incidencia_id=None):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')
    if profile.group_id == 1:
        if request.method == 'POST':
            inc_id = request.POST.get('incidencia_id')
            incidencia_a_actualizar = get_object_or_404(Incidencia, id=inc_id)
            incidencia_a_actualizar.departamento_id = request.POST.get('departamento')
            incidencia_a_actualizar.territorial_id = request.POST.get('territorial')
            incidencia_a_actualizar.encuesta_id = request.POST.get('encuesta')
            incidencia_a_actualizar.titulo = request.POST.get('titulo')
            incidencia_a_actualizar.tipo = request.POST.get('tipo')
            incidencia_a_actualizar.ubicacion = request.POST.get('ubicacion')
            incidencia_a_actualizar.save()
            messages.add_message(request, messages.INFO, 'Incidencia actualizada con éxito.')
            return redirect('main_incidencia')
        else:
            incidencia = get_object_or_404(Incidencia, id=incidencia_id)
            departamentos = Departamento.objects.all()
            territoriales = Territorial.objects.all()
            encuestas = Encuesta.objects.all()
            
            context = {
                'incidencia': incidencia,
                'departamentos': departamentos,
                'territoriales': territoriales,
                'encuestas': encuestas
            }
            return render(request, 'incidencia/editar_incidencia.html', context)
    else:
        return redirect('logout')

@login_required
def incidencias_usuario_departamento(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
        if profile.group_id != 3:
            print("--> RESULTADO: Permiso denegado. Redirigiendo...")
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('main_admin')
        print("--> RESULTADO: Permiso concedido. Buscando incidencias...")
        departamento_usuario = Departamento.objects.get(usuario=request.user)
        incidencias_asignadas = Incidencia.objects.filter(departamento=departamento_usuario)
        context = {
            'incidencias': incidencias_asignadas,
            'departamento': departamento_usuario,
        }
        return render(request, 'incidencia/incidencias_usuario_departamento.html', context)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')
    except Departamento.DoesNotExist:
        messages.error(request, 'No estás asignado a ningún departamento.')
        return redirect('main_admin')