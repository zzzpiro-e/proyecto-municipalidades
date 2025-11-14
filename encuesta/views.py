from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from registration.models import Profile
from .models import Encuesta
from departamento.models import Departamento
from pregunta.models import Pregunta

@login_required
def main_encuesta(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.error(request, 'Error de perfil.')
        return redirect('login')
    if profile.group_id == 1:
        encuestas = Encuesta.objects.select_related('departamento').order_by('-id')
        
        return render(request, 'encuesta/main_encuesta.html', context)

    elif profile.group_id == 3:
        try:
            departamento_usuario = Departamento.objects.get(usuario=request.user)
            encuestas = Encuesta.objects.filter(
                departamento=departamento_usuario
            ).select_related('departamento').order_by('-id')
        except Departamento.DoesNotExist:
            messages.error(request, 'No estás asignado a ningún departamento.')
            return redirect('main_departamento')
    else:
        return redirect('logout')
    context = {
            'encuestas': encuestas,
            'profile': profile
        }
    return render(request, 'encuesta/main_encuesta.html', {'encuestas': encuestas})


def crear_encuesta(request):
    try:
        profile= Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request,messages.INFO, 'Error')
        return redirect('login')
    if profile.group_id in [1,3]:
        departamentos=Departamento.objects.all()
        template_name = 'encuesta/crear_encuesta.html'
        return render(request,template_name,{"departamentos":departamentos,"es_admin":profile.group_id==1})
    else: 
        return redirect('logout')

@login_required
def bloquear_encuesta(request, pk):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.error(request, 'Error de perfil')
        return redirect('login')
    if profile.group_id in [1,3]:
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

@login_required
def guardar_encuesta(request):
    try:
        profile=Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO,"Error")
        return redirect('check_profile')
    if profile.group_id in [1,3]:
        if request.method=='POST':
            nombre_encuesta=request.POST.get('nombre_encuesta')
            departamento_id=request.POST.get('departamento')
            descripcion=request.POST.get("descripcion")
            tipo=request.POST.get("tipo")
            prioridad=request.POST.get("prioridad")

            if profile.group_id == 1:
                departamento_id = request.POST.get('departamento')
                if not departamento_id:
                    messages.add_message(request, messages.INFO, 'Debes seleccionar un departamento.')
                    return redirect('crear_encuesta')
            else:  
                try:
                    departamento = Departamento.objects.get(usuario=request.user)
                    departamento_id = departamento.id
                except Departamento.DoesNotExist:
                    messages.error(request, "Tu usuario no está asociado a ningún departamento.")
                    return redirect('crear_encuesta')

            if nombre_encuesta=='' or not departamento_id:
                messages.add_message(request,messages.INFO, 'Debes ingresar toda la información, no pueden quedar campos vacíos')
                return redirect('crear_encuesta')
            encuesta_save=Encuesta(
                nombre_encuesta=nombre_encuesta,
                departamento_id=departamento_id,
                tipo=tipo,
                prioridad=prioridad,
                descripcion=descripcion,
                )
            encuesta_save.save()

            preguntas = request.POST.getlist('preguntas[]')
            for titulo in preguntas:
                if titulo.strip(): 
                    Pregunta.objects.create(encuesta=encuesta_save, titulo=titulo)

            messages.add_message(request,messages.INFO,'encuesta creada con exito')
            return redirect('main_encuesta')
        else:
            messages.add_message(request,messages.INFO,'No se pudo realizar la solicitud, intente nuevamente')
            return redirect('check_group_main')
    else:
        return redirect('logout')

@login_required
def editar_encuesta(request, encuesta_id=None):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')
    if profile.group_id in [1,3]:
        if request.method == 'POST':
            encuesta_id_post = request.POST.get('encuesta_id')
            encuesta_a_actualizar = get_object_or_404(Encuesta, id=encuesta_id_post)
            if encuesta_a_actualizar.state != 'Bloqueado':
                messages.warning(request, 'Solo se pueden editar encuestas bloqueadas.')
                return redirect('main_encuesta')
            encuesta_a_actualizar.nombre_encuesta = request.POST.get('nombre_encuesta')
            encuesta_a_actualizar.descripcion = request.POST.get('descripcion')
            encuesta_a_actualizar.tipo = request.POST.get('tipo')
            encuesta_a_actualizar.prioridad = request.POST.get('prioridad')
            encuesta_a_actualizar.departamento_id = request.POST.get('departamento')
            encuesta_a_actualizar.save()
            preguntas_ids = request.POST.getlist('pregunta_id[]')
            preguntas_textos = request.POST.getlist('pregunta_texto[]')
            for pid, texto in zip(preguntas_ids, preguntas_textos):
                if texto.strip():
                    pregunta = get_object_or_404(Pregunta, id=pid)
                    pregunta.titulo = texto
                    pregunta.save()
            nuevas_preguntas = request.POST.getlist('nuevas_preguntas[]')
            for titulo in nuevas_preguntas:
                if titulo.strip():
                    Pregunta.objects.create(encuesta=encuesta_a_actualizar, titulo=titulo)
            messages.add_message(request, messages.INFO, 'Encuesta actualizada con éxito.')
            return redirect('main_encuesta')
        else:
            encuesta_para_editar = get_object_or_404(Encuesta, id=encuesta_id)
            if encuesta_para_editar.state != 'Bloqueado':
                messages.warning(request, 'Solo se pueden editar encuestas bloqueadas.')
                return redirect('main_encuesta')
            departamentos = Departamento.objects.all()
            preguntas=Pregunta.objects.filter(encuesta=encuesta_para_editar)
            template_name = 'encuesta/editar_encuesta.html'
            context = {
                'encuesta': encuesta_para_editar,
                'departamentos': departamentos,
                'preguntas':preguntas
            }
            return render(request, template_name, context)
    else:
        return redirect('logout')
