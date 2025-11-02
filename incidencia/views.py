from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from registration.models import Profile
from .models import Incidencia, MultimediaIncidencia 
from departamento.models import Departamento
from territorial.models import Territorial
from encuesta.models import Encuesta
from django.contrib.auth.models import User

@login_required
def main_incidencia(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')

    if profile.group_id ==4:
        incidencias = Incidencia.objects.filter(state='Activo').select_related('departamento', 'territorial').order_by('-id')
        context = {
            'incidencias': incidencias,
            'profile': profile
        }
        return render(request, 'incidencia/main_incidencia.html', context)
    else:
        return redirect('logout')

@login_required
def gestion_incidencia(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')

    if profile.group_id in [1, 2, 3, 4, 5]:
        incidencias = Incidencia.objects.filter(state='Activo').select_related('departamento', 'territorial').order_by('-id')
        context = {
            'incidencias': incidencias,
            'profile': profile
        }
        return render(request, 'incidencia/gestion_incidencia.html', context)
    else:
        return redirect('logout')

@login_required
def crear_incidencia(request):
    try:
        profile = Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO, "Error al obtener el perfil del usuario.")
        return redirect('check_profile')
    if profile.group_id == 4:
        template_name = 'incidencia/crear_incidencia.html'
        departamentos = Departamento.objects.all()
        encuestas = Encuesta.objects.all()
        context = {
            'departamentos': departamentos,
            'encuestas': encuestas
        }

        return render(request, template_name, context)
    else:
        return redirect('logout')

@login_required
def guardar_incidencia(request):
    try:
        profile=Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO,"Error")
        return redirect('check_profile')
    if profile.group_id==4:
        if request.method=='POST':
            departamento_id=request.POST.get('departamento')
            titulo=request.POST.get('titulo')
            tipo=request.POST.get("tipo")
            ubicacion=request.POST.get("ubicacion")
            latitud=request.POST.get("latitud")
            longitud=request.POST.get("longitud")
            nombre_vecino=request.POST.get("nombre_vecino")
            telefono_vecino=request.POST.get("telefono_vecino")
            correo_vecino=request.POST.get("correo_vecino")
            encuesta_id=request.POST.get("encuesta")
            if titulo=='' or latitud=="" or longitud=="" or not departamento_id :
                messages.add_message(request,messages.INFO, 'Debes ingresar toda la información, no pueden quedar campos vacíos')
                return redirect('crear_incidencia')
            try:
                territorial = Territorial.objects.get(usuario=request.user)
            except Territorial.DoesNotExist:
                messages.add_message(request, messages.INFO, 'No tienes un registro territorial asignado.')
                return redirect('check_profile')
            incidencia_save=Incidencia(
                territorial=territorial,
                titulo=titulo,
                departamento_id=departamento_id,
                tipo=tipo,
                ubicacion=ubicacion,
                latitud=latitud,
                longitud=longitud,
                nombre_vecino=nombre_vecino,
                telefono_vecino=telefono_vecino,
                correo_vecino=correo_vecino,
                encuesta_id=encuesta_id
            )
            incidencia_save.save() 
            archivos_subidos = request.FILES.getlist('archivos')
            
            for archivo in archivos_subidos:
                MultimediaIncidencia.objects.create(
                    incidencia=incidencia_save,
                    tipo=archivo.content_type,
                    path=archivo
                )
            messages.add_message(request,messages.INFO,'Incidencia y archivos creados con éxito.')
            return redirect('main_incidencia')
        else:
            messages.add_message(request,messages.INFO,'No se pudo realizar la solicitud, intente nuevamente')
            return redirect('check_group_main')
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
            messages.success(request, f'La incidencia "{incidencia.titulo}" fue bloqueada.')
        else:
            incidencia.state = 'Activo'
            messages.success(request, f'La incidencia "{incidencia.titulo}" fue activada.')
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
            messages.error(request, 'No tienes permiso para acceder a esta página.')
            return redirect('main_admin')
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

@login_required
def ver_incidencia(request, incidencia_id):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
        if profile.group_id in [1, 2, 3, 4, 5]:
            incidencia = get_object_or_404(Incidencia, id=incidencia_id)
            context = {
                'incidencia': incidencia
            }
            return render(request, 'incidencia/ver_incidencia.html', context)
        else:
            messages.error(request, 'No tienes permiso para ver esta página.')
            return redirect('main_admin')
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')