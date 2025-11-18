from django.shortcuts import render, redirect
from .models import ArchivoMultimedia

def subir_archivo(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        tipo = request.POST.get('tipo')
        archivo = request.FILES.get('archivo')

        if titulo and tipo and archivo:  # Validación básica
            ArchivoMultimedia.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                tipo=tipo,
                archivo=archivo
            )
            return redirect('subir_archivo')

    return render(request, 'multimedia/subir.html')


