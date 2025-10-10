from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from registration.models import Profile
from .models import Encuesta
from departamento.models import Departamento

@login_required
def main_encuesta(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.error(request, 'Error de perfil.')
        return redirect('login')
    if profile.group_id in [1, 2, 3, 4, 5]:
        encuestas = Encuesta.objects.select_related('departamento').order_by('-id')
        return render(request, 'encuesta/main_encuesta.html', {'encuestas': encuestas})
    else:
        return redirect('logout')


@login_required
def bloquear_encuesta(request, pk):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.error(request, 'Error de perfil')
        return redirect('login')

    if profile.group_id == 1:
        encuesta = get_object_or_404(Encuesta, id=pk)
        if encuesta.state == 'Activo':
            encuesta.state = 'Bloqueado'
            messages.success(request, f"La encuesta '{encuesta.nombre_encuesta}' fue bloqueada correctamente.")
        else:
            encuesta.state = 'Activo'
            messages.success(request, f"La encuesta '{encuesta.nombre_encuesta}' fue activada correctamente.")
        encuesta.save()
        return redirect('main_encuesta')
    else:
        return redirect('logout')
