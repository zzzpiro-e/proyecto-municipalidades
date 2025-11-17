from django.shortcuts import render, redirect, get_object_or_404
from .models import ArchivoMultimedia
from incidencia.models import Incidencia

def subir_archivo(request, registro_id): 
    registro_trabajo = get_object_or_404(Incidencia, pk=registro_id) 

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        tipo = request.POST.get('tipo')
        archivo = request.FILES.get('archivo')

        if titulo and tipo and archivo: # Validación básica
            ArchivoMultimedia.objects.create(
                registro_trabajo=registro_trabajo,
                titulo=titulo,
                descripcion=descripcion,
                tipo=tipo,
                archivo=archivo
            )


            return redirect('detalle_registro', pk=registro_id) 

    context = {'registro_id': registro_id}
    return render(request, 'multimedia/subir.html', context)


