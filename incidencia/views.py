from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from registration.models import Profile
from .models import Incidencia, MultimediaIncidencia 
from departamento.models import Departamento
from territorial.models import Territorial
from encuesta.models import Encuesta
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from pregunta.models import Pregunta, Respuesta
from asignacion.models import Asignacion

@login_required
def gestion_incidencia(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')

    if profile.group_id in [1, 2, 3, 4, 5]:

        estado_filtro = request.GET.get("estado", "Todos")

        qs = Incidencia.objects.filter(state='Activo').select_related(
            'departamento', 'territorial'
        ).order_by('estado')

        if profile.group_id == 4:  
            try:
                territorial = Territorial.objects.get(usuario=request.user)
                qs = qs.filter(territorial=territorial)
            except Territorial.DoesNotExist:
                qs = qs.none()

        if estado_filtro != "Todos":
            qs = qs.filter(estado=estado_filtro)

        paginator = Paginator(qs, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            'incidencias': page_obj,     
            'profile': profile,

            'estado_actual': estado_filtro,
            'page_obj': page_obj,        

        }
        return render(request, 'incidencia/gestion_incidencia.html', context)


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
            
            if titulo=='' or latitud==""  or longitud=="" or not departamento_id :
                messages.add_message(request,messages.INFO, 'Debes ingresar toda la información, no pueden quedar campos vacíos')
                return redirect('crear_incidencia')
            
            lat = float(request.POST.get('latitud'))
            lon = float(request.POST.get('longitud'))

            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                messages.error(request, "Debes ingresar datos validos, revisa las coordenadas.")
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

            preguntas = Pregunta.objects.filter(encuesta_id=encuesta_id)
            
            for p in preguntas:
                campo = f"respuesta_{p.id}"
                contenido = request.POST.get(campo, "").strip()

                if contenido:
                    Respuesta.objects.create(
                    incidencia=incidencia_save,
                    pregunta=p,
                    contenido=contenido
                )

            archivos_subidos = request.FILES.getlist('archivos')
            
            for archivo in archivos_subidos:
                content_type = archivo.content_type
                tipo_simple = 'otro'
                if content_type.startswith('image'):
                    tipo_simple = 'imagen'
                elif content_type.startswith('video'):
                    tipo_simple = 'video'
                elif content_type.startswith('audio'):
                    tipo_simple = 'audio'
                
                MultimediaIncidencia.objects.create(
                    incidencia=incidencia_save,
                    tipo=tipo_simple,
                    path=archivo
                )
            messages.add_message(request,messages.INFO,'Incidencia creada con éxito.')
            return redirect('main_territorial')
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

    if profile.group_id in [1,4]: 
        incidencia = get_object_or_404(Incidencia, id=pk)
        if incidencia.state == 'Activo':
            incidencia.state = 'Bloqueado'
            messages.success(request, f'La incidencia "{incidencia.titulo}" fue bloqueada.')
        elif incidencia.state == 'Bloqueado' and incidencia.estado == 'Rechazada':
            incidencia.estado='Pendiente'
            incidencia.state = 'Activo'
            messages.success(request, f'La incidencia "{incidencia.titulo}" fue activada.')
        elif incidencia.state == 'Bloqueado':
            incidencia.state = 'Activo'
            messages.success(request, f'La incidencia "{incidencia.titulo}" fue activada.')
        incidencia.save()
        return redirect('gestion_incidencia')
    return redirect('logout')

@login_required
def ver_incidencias_bloqueo(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.error(request, 'Error de perfil')
        return redirect('login')

    if profile.group_id not in [1, 4]:
        return redirect('logout')
    qs = Incidencia.objects.filter(state='Bloqueado').select_related(
        'departamento', 'territorial', 'encuesta'
    )
    if profile.group_id == 4:
        try:
            territorial = Territorial.objects.get(usuario=request.user)
            qs = qs.filter(territorial=territorial)
        except Territorial.DoesNotExist:
            qs = qs.none()

    return render(request, 'incidencia/bloquear_incidencias.html', {
        'incidencias': qs
    })

@login_required
def editar_incidencia(request, incidencia_id=None):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')
    
    if profile.group_id == 1 or profile.group_id == 4:

        if request.method == 'POST':

            inc_id = request.POST.get('incidencia_id')
            incidencia_a_actualizar = get_object_or_404(Incidencia, id=inc_id)

            # ← Debes volver a obtener las respuestas aquí
            respuestas = Respuesta.objects.filter(
                incidencia=incidencia_a_actualizar
            ).select_related("pregunta")

            incidencia_a_actualizar.departamento_id = request.POST.get('departamento')
            incidencia_a_actualizar.territorial_id = request.POST.get('territorial')
            incidencia_a_actualizar.encuesta_id = request.POST.get('encuesta')
            incidencia_a_actualizar.titulo = request.POST.get('titulo')
            incidencia_a_actualizar.tipo = request.POST.get('tipo')
            incidencia_a_actualizar.ubicacion = request.POST.get('ubicacion')
            incidencia_a_actualizar.save()

            for r in respuestas:
                nuevo_contenido = request.POST.get(f"respuesta_{r.pregunta.id}", "").strip()
                r.contenido = nuevo_contenido
                r.save()

            messages.add_message(request, messages.INFO, 'Incidencia actualizada con éxito.')
            return redirect('gestion_incidencia')

        else:
            incidencia = get_object_or_404(Incidencia, id=incidencia_id)

            respuestas = Respuesta.objects.filter(
                incidencia=incidencia
            ).select_related("pregunta")

            departamentos = Departamento.objects.all()
            territoriales = Territorial.objects.all()
            encuestas = Encuesta.objects.all()

            context = {
                'incidencia': incidencia,
                'departamentos': departamentos,
                'territoriales': territoriales,
                'encuestas': encuestas,
                'respuestas': respuestas
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
            return redirect('logout')
            
        departamento_usuario = Departamento.objects.get(usuario=request.user)

        
        estado_filtro = request.GET.get("estado", "Todos") 

        qs = Incidencia.objects.filter(departamento=departamento_usuario)

        if estado_filtro != "Todos":
            qs = qs.filter(estado=estado_filtro)
        
        

        paginator = Paginator(qs.order_by('estado'), 6)  
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            'incidencias': page_obj,
            'departamento': departamento_usuario,
            'estado_actual': estado_filtro,
            'page_obj': page_obj
        }

        return render(request, 'incidencia/incidencias_usuario_departamento.html', context)

    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')

    except Departamento.DoesNotExist:
        messages.error(request, 'No estás asignado a ningún departamento.')
        return redirect('logout')


@login_required
def ver_incidencia(request, incidencia_id):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
        if profile.group_id in [1, 2, 3, 4, 5]:
            incidencia = get_object_or_404(Incidencia, id=incidencia_id)
            fallback_url = reverse('main_admin') 
            back_url = request.META.get('HTTP_REFERER', fallback_url)
            
            preguntas = incidencia.encuesta.preguntas.all()
            respuestas = incidencia.respuesta_set.all()
            encuestas = Encuesta.objects.filter(incidencia=incidencia)
            respuestas_por_pregunta = {
            r.pregunta_id: r for r in respuestas
            }

            context = {
                'incidencia': incidencia,
                'back_url': back_url,
                'preguntas':preguntas,
                'respuestas_por_pregunta':respuestas_por_pregunta, 
                'encuestas':encuestas  
            }
            return render(request, 'incidencia/ver_incidencia.html', context)
        else:
            messages.error(request, 'No tienes permiso para ver esta página.')
            return redirect('logout')
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')
    
@login_required
def rechazar_incidencia(request, pk):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.error(request, 'Error de perfil')
        return redirect('login')
    if profile.group_id == 3: 
        incidencia = get_object_or_404(Incidencia, id=pk)
        incidencia.estado = "Rechazada"
        incidencia.state = "Bloqueado"
        incidencia.save()
        asignacion = Asignacion.objects.filter(incidencia=incidencia).first()
        if asignacion:
            asignacion.delete()
        messages.success(request, f'La incidencia "{incidencia.titulo}" fue rechazada.')
        return redirect('incidencias_usuario_departamento')
    else:
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('logout')
    
@login_required
def eliminar_incidencia(request, incidencia_id):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.error(request, 'Error de perfil')
        return redirect('login')
    if profile.group_id != 4:
        return redirect('logout')
    incidencia = get_object_or_404(Incidencia, pk=incidencia_id)
    if incidencia.estado == 'Resuelta':
        messages.error(request, 'No puedes eliminar una incidencia que ya está resuelta.')
        return redirect('gestion_incidencia')
    asignacion = Asignacion.objects.filter(incidencia=incidencia).first()
    if asignacion:
        asignacion.delete()
    titulo = incidencia.titulo
    incidencia.delete()

    messages.success(request, f'La incidencia "{titulo}" fue eliminada con éxito.')
    return redirect('gestion_incidencia')