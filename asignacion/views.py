from django.shortcuts import render,get_object_or_404,redirect
from cuadrilla.models import Cuadrilla
from incidencia.models import Incidencia
from .models import Asignacion

def asignar_incidencia(request, cuadrilla_id):
    cuadrilla = get_object_or_404(Cuadrilla, id=cuadrilla_id)
    incidencias = Incidencia.objects.filter(
        departamento=cuadrilla.departamento
    ).exclude(id__in=Asignacion.objects.values('incidencia_id'))

    if request.method == "POST":
        incidencia_id = request.POST.get("incidencia_id")
        incidencia = get_object_or_404(Incidencia, id=incidencia_id)

        # Crear el vínculo en la tabla intermedia
        Asignacion.objects.create(
            cuadrilla=cuadrilla,
            incidencia=incidencia,
        )

        incidencia.estado = "asignada"
        incidencia.save()

        return redirect("main_departamento")

    return render(request, "departamento/asignar_incidencia.html", {
        "cuadrilla": cuadrilla,
        "incidencias": incidencias
    })
