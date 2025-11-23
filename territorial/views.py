from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from registration.models import Profile
from .models import Territorial
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from incidencia.models import Incidencia

@login_required
def main_territorial(request):
    try:
        territorial = Territorial.objects.get(usuario=request.user)
    except Territorial.DoesNotExist:
        messages.error(request, "No tienes registro territorial asociado.")
        return redirect("login")
    incidencias = Incidencia.objects.filter(territorial=territorial)
    total = incidencias.count()
    pendientes = incidencias.filter(estado="Pendiente").count()
    asignadas = incidencias.filter(estado="Asignada").count()
    resueltas = incidencias.filter(estado="Resuelta").count()
    rechazadas = incidencias.filter(estado="Rechazada").count()

    context = {
        "total": total,
        "pendientes": pendientes,
        "asignadas": asignadas,
        "resueltas": resueltas,
        "rechazadas": rechazadas,
        "territorial": territorial,
    }

    return render(request, "territorial/main_territorial.html", context)


@login_required
def editar_territorial(request, territorial_id=None):
    try:
        profile = Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO, 'Error de perfil')
        return redirect('login')
    if profile.group_id == 1:
        if request.method == 'POST':
            terr_id = request.POST.get('territorial_id')
            usuario_id = request.POST.get("usuario")
            zona_asignada = request.POST.get('zona_asignada')
            observaciones = request.POST.get('observaciones')
            territorial_a_actualizar = get_object_or_404(Territorial, id=terr_id)
            territorial_a_actualizar.usuario_id = usuario_id
            territorial_a_actualizar.zona_asignada = zona_asignada
            territorial_a_actualizar.observaciones = observaciones
            territorial_a_actualizar.save()
            messages.add_message(request, messages.INFO, 'Territorial actualizado con éxito.')
            return redirect('main_territorial')
        else:
            territorial = get_object_or_404(Territorial, id=territorial_id)
            usuarios = User.objects.filter(profile__group__id=4)
            template_name = 'territorial/editar_territorial.html'
            context = {
                'territorial': territorial,
                'usuarios': usuarios
            }
            return render(request, template_name, context)
    else:
        return redirect('logout')




    


    


