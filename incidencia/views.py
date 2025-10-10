from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from registration.models import Profile
from .models import Incidencia 
@login_required
def main_incidencia(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil')
        return redirect('login')

    if profile.group_id in [1, 2, 3, 4, 5]:
        incidencias = Incidencia.objects.select_related('departamento', 'territorial').all().order_by('-id')
        template_name = 'incidencia/main_incidencia.html'
        context = {'incidencias': incidencias}
        return render(request, template_name, context)
    else:
        return redirect('logout')


@login_required
def bloquear_incidencia(request, pk):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.error(request, 'Error de perfil')
        return redirect('login')

    if profile.group_id == 1: 
        incidencia = get_object_or_404(Incidencia, id=pk)
        if incidencia.state == 'Activo':
            incidencia.state = 'Bloqueado'
            messages.success(request, f'La incidencia "{incidencia.id}" fue bloqueada.')
        else:
            incidencia.state = 'Activo'
            messages.success(request, f'La incidencia "{incidencia.id}" fue activada.')
        incidencia.save()
        return redirect('main_incidencia')
    return redirect('logout')


@login_required
def ver_incidencias_bloqueo(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.error(request, 'Error de perfil')
        return redirect('login')

    if profile.group_id == 1:
        incidencias = Incidencia.objects.filter(state='Bloqueado').select_related('departamento', 'territorial', 'encuesta')
        return render(request, 'incidencia/bloquear_incidencias.html', {'incidencias': incidencias})
    return redirect('logout')
