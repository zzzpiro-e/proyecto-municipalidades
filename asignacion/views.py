from django.shortcuts import render,get_object_or_404,redirect
from cuadrilla.models import Cuadrilla
from incidencia.models import Incidencia
from registration.models import Profile
from django.contrib import messages
from .models import Asignacion
from django.contrib.auth.decorators import login_required

@login_required
def asignar_incidencia(request, cuadrilla_id):
    
    profile=Profile.objects.filter(user_id=request.user.id).get()
    if profile.group_id != 3:
        messages.error(request, "No tienes permiso para asignar incidencias.")
        return redirect("logout")
    
    cuadrilla = get_object_or_404(Cuadrilla, id=cuadrilla_id)
    incidencias = Incidencia.objects.filter(
        departamento=cuadrilla.departamento,state='Activo'
    ).exclude(id__in=Asignacion.objects.values('incidencia_id'))

    if request.method == "POST":
        incidencia_id = request.POST.get("incidencia_id")
        incidencia = get_object_or_404(Incidencia, id=incidencia_id)

        
        Asignacion.objects.create(
            cuadrilla=cuadrilla,
            incidencia=incidencia,
        )

        incidencia.estado = "Asignada"
        incidencia.save()

        return redirect("main_departamento")

    return render(request, "departamento/asignar_incidencia.html", {
        "cuadrilla": cuadrilla,
        "incidencias": incidencias
    })
