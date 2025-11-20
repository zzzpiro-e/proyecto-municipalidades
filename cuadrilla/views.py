from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from registration.models import Profile
from cuadrilla.models import Cuadrilla, Registro_trabajo
from departamento.models import Departamento
from incidencia.models import Incidencia
from asignacion.models import Asignacion
from django.contrib.auth.models import User
from django.core.paginator import Paginator


@login_required
def main_cuadrilla(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error')
        return redirect('login')

    if profile.group_id ==5:
        cuadrillas = (Cuadrilla.objects.select_related('usuario', 'departamento').order_by('id'))
        return render(request, 'cuadrilla/main_cuadrilla.html', {'cuadrillas': cuadrillas})
    else:
        return redirect('logout')

@login_required
def gestion_cuadrilla(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error')
        return redirect('login')

    if profile.group_id == 1:

        cuadrillas_list = (
            Cuadrilla.objects
            .select_related('usuario', 'departamento')
            .order_by('id')
        )

        paginator = Paginator(cuadrillas_list, 6)
        page_number = request.GET.get('page')
        cuadrillas = paginator.get_page(page_number)

        return render(
            request,
            'cuadrilla/gestion_cuadrilla.html',
            {
                'cuadrillas': cuadrillas,
                'profile': profile
            }
        )

    else:
        return redirect('logout')
    
def crear_cuadrilla(request):
    try:
        profile= Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request,messages.INFO, 'Error')
        return redirect('login')
    if profile.group_id ==1:
        departamentos=Departamento.objects.all()
        template_name = 'cuadrilla/crear_cuadrilla.html'
        usuarios=User.objects.filter(profile__group__id=5, cuadrilla__isnull=True)
        return render(request,template_name,{"departamentos":departamentos, "usuarios":usuarios})
    else: 
        return redirect('logout')


@login_required
def guardar_cuadrilla(request):
    try:
        profile=Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO,"Error")
        return redirect('check_profile')
    if profile.group_id==1:
        if request.method=='POST':
            nombre_cuadrilla=request.POST.get('nombre_cuadrilla')
            tipo=request.POST.get('tipo')
            departamento_id=request.POST.get('departamento')
            usuario_id=request.POST.get("usuario")

            if nombre_cuadrilla=='' or not departamento_id or not usuario_id or tipo=="":
                messages.add_message(request,messages.INFO, 'Debes ingresar toda la información, no pueden quedar campos vacíos')
                return redirect('crear_cuadrilla')
            cuadrilla_save=Cuadrilla(
                nombre_cuadrilla=nombre_cuadrilla,
                departamento_id=departamento_id,
                usuario_id=usuario_id,
                tipo=tipo
                )
            cuadrilla_save.save()
            messages.add_message(request,messages.INFO,'cuadrilla creado con exito')
            return redirect('gestion_cuadrilla')
        else:
            messages.add_message(request,messages.INFO,'No se pudo realizar la solicitud, intente nuevamente')
            return redirect('check_group_main')
    else:
        return redirect('logout')

@login_required
def editar_cuadrilla(request, cuadrilla_id=None):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')

    if profile.group_id != 1:
        return redirect('logout')

    if request.method == 'POST':
        cua_id = request.POST.get('cuadrilla_id')
        nombre_cuadrilla = request.POST.get('nombre_cuadrilla')
        tipo=request.POST.get('tipo')
        departamento_id = request.POST.get('departamento')
        usuario_id = request.POST.get("usuario")

        cuadrilla_a_actualizar = get_object_or_404(Cuadrilla, id=cua_id)

        # Validación: si se intentó seleccionar un usuario que ya tiene cuadrilla distinto al actual -> bloquear
        usuario_ya_asignado = Cuadrilla.objects.filter(usuario_id=usuario_id).exclude(id=cua_id).exists()
        if usuario_ya_asignado:
            messages.add_message(request, messages.INFO, 'El usuario seleccionado ya tiene otra cuadrilla asignada.')
            return redirect('editar_cuadrilla', cuadrilla_id=cua_id)

        cuadrilla_a_actualizar.nombre_cuadrilla = nombre_cuadrilla
        cuadrilla_a_actualizar.tipo = tipo
        cuadrilla_a_actualizar.departamento_id = departamento_id
        cuadrilla_a_actualizar.usuario_id = usuario_id
        cuadrilla_a_actualizar.save()

        messages.add_message(request, messages.INFO, 'cuadrilla actualizada con éxito.')
        return redirect('gestion_cuadrilla')

    else:
        cuadrilla_para_editar = get_object_or_404(Cuadrilla, id= cuadrilla_id)
        departamentos = Departamento.objects.all()
        # Mostrar sólo usuarios del grupo 3 que NO tienen cuadrilla asignado (misma lógica que crear)
        usuarios = User.objects.filter(profile__group__id=5)

        template_name = 'cuadrilla/editar_cuadrilla.html'
        context = {
            'cuadrilla': cuadrilla_para_editar,
            'departamentos': departamentos,
            'usuarios': usuarios
        }
        return render(request, template_name, context)

@login_required
def ver_cuadrilla(request, cuadrilla_id: int):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error')
        return redirect('login')

    if profile.group_id not in [1, 5]:
        return redirect('logout')
    
    cuadrilla = get_object_or_404(
        Cuadrilla.objects.select_related('usuario','departamento'),
        pk=cuadrilla_id
    )
    return render(request, 'cuadrilla/ver_cuadrilla.html', {'cuadrillas': cuadrilla})

@login_required
def bloquear_cuadrilla(request, pk):
    try:
        profile = Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO, 'Error')
        return redirect('login')

    if profile.group_id == 1:  
        cuadrilla = get_object_or_404(Cuadrilla, pk=pk)
        if cuadrilla.state == "Activo":
            cuadrilla.state = "Inactivo"
            messages.add_message(request, messages.SUCCESS, f"La cuadrilla {cuadrilla.nombre_cuadrilla} fue bloqueada.")
        else:
            cuadrilla.state = "Activo"
            messages.add_message(request, messages.SUCCESS, f"La cuadrilla {cuadrilla.nombre_cuadrilla} fue activada.")
        cuadrilla.save()
        return redirect('gestion_cuadrilla')
    else:
        return redirect('logout')

@login_required
def crear_registro(request):
    try:
        cuadrilla = Cuadrilla.objects.get(usuario=request.user)
    except Cuadrilla.DoesNotExist:
        messages.error(request, "Tu usuario no está asociado a ninguna cuadrilla.")
        return redirect('home')

    incidencias = Incidencia.objects.filter(
        asignacion__cuadrilla=cuadrilla
    ).exclude(id__in=Registro_trabajo.objects.values_list('incidencia_id', flat=True))

    if request.method == 'POST':
        incidencia_id = request.POST.get('incidencia')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha')

        if not incidencia_id:
            messages.error(request, "Debes seleccionar una incidencia.")
            return redirect('crear_registro')

        incidencia = get_object_or_404(Incidencia, id=incidencia_id)

        Registro_trabajo.objects.create(
            incidencia=incidencia,
            cuadrilla=cuadrilla,
            descripcion=descripcion,
            fecha=fecha
        )


        incidencia.state = Incidencia.STATE_RESUELTO
        incidencia.save()

        messages.success(request, "Registro creado correctamente.")
        return redirect('main_cuadrilla')

    return render(request, 'cuadrilla/crear_registro.html', {
        'incidencias': incidencias,
        'cuadrilla': cuadrilla
    })


def ver_incidencias_cuadrilla(request):
    cuadrilla = Cuadrilla.objects.filter(usuario=request.user).first()

    asignaciones_qs = Asignacion.objects.filter(cuadrilla=cuadrilla).select_related('incidencia')


    paginator = Paginator(asignaciones_qs, 6)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'asignaciones': page_obj
    }
    return render(request, 'cuadrilla/ver_incidencias_cuadrilla.html', context)

def ver_registro(request):
    cuadrilla = Cuadrilla.objects.filter(usuario=request.user).first()
    registros = Registro_trabajo.objects.filter(cuadrilla=cuadrilla).order_by('-fecha')
    return render(request, 'cuadrilla/ver_registro.html', {'registros': registros})
