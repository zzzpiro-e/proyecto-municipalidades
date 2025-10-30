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
        context = {
            'encuestas': encuestas,
            'profile': profile
        }
        return render(request, 'encuesta/main_encuesta.html', context)
    else:
        return redirect('logout')

def crear_encuesta(request):
    try:
        profile= Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request,messages.INFO, 'Error')
        return redirect('login')
    if profile.group_id ==3:
        departamentos=Departamento.objects.all()
        template_name = 'encuesta/crear_encuesta.html'
        return render(request,template_name,{"departamentos":departamentos})
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

@login_required
def guardar_encuesta(request):
    try:
        profile=Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO,"Error")
        return redirect('check_profile')
    if profile.group_id==3:
        if request.method=='POST':
            nombre_encuesta=request.POST.get('nombre_encuesta')
            departamento_id=request.POST.get('departamento')
            descripcion=request.POST.get("descripcion")
            tipo=request.POST.get("tipo")
            prioridad=request.POST.get("prioridad")
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
            messages.add_message(request,messages.INFO,'encuesta creado con exito')
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
    if profile.group_id == 1:
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
            messages.add_message(request, messages.INFO, 'Encuesta actualizada con éxito.')
            return redirect('main_encuesta')
        else:
            encuesta_para_editar = get_object_or_404(Encuesta, id=encuesta_id)
            if encuesta_para_editar.state != 'Bloqueado':
                messages.warning(request, 'Solo se pueden editar encuestas bloqueadas.')
                return redirect('main_encuesta')
            departamentos = Departamento.objects.all()
            template_name = 'encuesta/editar_encuesta.html'
            context = {
                'encuesta': encuesta_para_editar,
                'departamentos': departamentos
            }
            return render(request, template_name, context)
    else:
        return redirect('logout')
