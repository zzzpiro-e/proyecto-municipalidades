from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from registration.models import Profile
from direccion.models import Direccion
from django.contrib.auth.models import User
from departamento.models import Departamento
from incidencia.models import Incidencia
from django.core.paginator import Paginator


@login_required
def main_direccion(request):
    try:
        direccion = Direccion.objects.get(usuario=request.user)
    except Direccion.DoesNotExist:
        messages.error(request, "No tienes direccion asociado.")
        return redirect("login")
    incidencias = Incidencia.objects.filter(departamento__direccion=direccion)
    total = incidencias.count()
    pendientes = incidencias.filter(estado="Pendiente").count()
    asignadas = incidencias.filter(estado="Asignada").count()
    resueltas = incidencias.filter(estado="Resuelta").count()
    rechazadas = incidencias.filter(estado="Rechazada").count()

    departamentos=Departamento.objects.filter(direccion=direccion)
    departamentos_totales=departamentos.count()
    context = {
        "total": total,
        "pendientes": pendientes,
        "asignadas": asignadas,
        "resueltas": resueltas,
        "rechazadas": rechazadas,
        "departamentos_totales":departamentos_totales,
        "direccion": direccion,
    }

    return render(request, "direccion/main_direccion.html", context)

@login_required
def gestion_direccion(request, direccion_id=None):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error')
        return redirect('login')

    if profile.group_id == 1:
        direccion_listado = Direccion.objects.select_related('usuario').order_by('id')

        paginator = Paginator(direccion_listado, 6)
        page_number = request.GET.get('page')
        direcciones = paginator.get_page(page_number)

        return render(
            request,
            'direccion/gestion_direccion.html',
            {'direcciones': direcciones}
        )
    else:
        return redirect('logout')


def crear_direccion(request):
    try:
        profile= Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request,messages.INFO, 'Error')
        return redirect('login')
    if profile.group_id ==1:
        template_name = 'direccion/crear_direccion.html'
        usuarios=User.objects.filter(profile__group__id=2, direccion__isnull=True)
        return render(request,template_name,{"usuarios":usuarios})
    else: 
        return redirect('logout')

@login_required
def guardar_direccion(request):
    try:
        profile=Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO,"Error")
        return redirect('check_profile')
    if profile.group_id==1:
        if request.method=='POST':
            nombre_direccion=request.POST.get('nombre_direccion')
            usuario_id=request.POST.get("usuario")
            if nombre_direccion=='' or not usuario_id:
                messages.add_message(request,messages.INFO, 'Debes ingresar toda la información, no pueden quedar campos vacíos')
                return redirect('crear_direccion')
            usuario_ocupado = Direccion.objects.filter(usuario_id=usuario_id).exists()
            if usuario_ocupado:
                messages.warning(request, 'Error: El usuario seleccionado ya es encargado de otra Dirección.')
                return redirect('crear_direccion')
            direccion_save=Direccion(
                nombre_direccion=nombre_direccion,
                usuario_id=usuario_id,
                )
            direccion_save.save()
            messages.add_message(request,messages.INFO,'Dirección creada con exito')
            return redirect('gestion_direccion')
        else:
            messages.add_message(request,messages.INFO,'No se pudo realizar la solicitud, intente nuevamente')
            return redirect('check_group_main')
    else:
        return redirect('logout')
    
@login_required
def editar_direccion(request, direccion_id=None):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')

    if profile.group_id != 1:
        return redirect('logout')

    if request.method == 'POST':
        dir_id = request.POST.get('direccion_id')
        nombre_direccion = request.POST.get('nombre_direccion')
        usuario_id = request.POST.get("usuario")

        direccion_a_actualizar = get_object_or_404(Direccion, id=dir_id)
        usuario_ya_asignado = Direccion.objects.filter(usuario_id=usuario_id).exclude(id=dir_id).exists()
        if usuario_ya_asignado:
            messages.add_message(request, messages.INFO, 'El usuario seleccionado ya tiene otra direccion asignada.')
            return redirect('editar_direccion', direccion_id=dir_id)

        direccion_a_actualizar.nombre_direccion = nombre_direccion
        direccion_a_actualizar.usuario_id = usuario_id
        direccion_a_actualizar.save()

        messages.add_message(request, messages.INFO, 'direccion actualizada con éxito.')
        return redirect('gestion_direccion')

    else:
        direccion_para_editar = get_object_or_404(Direccion, id=direccion_id)
        direcciones = Direccion.objects.all()
        usuarios = User.objects.filter(profile__group__id=2)

        template_name = 'direccion/editar_direccion.html'
        context = {
            'direccion': direccion_para_editar,
            'direcciones': direcciones,
            'usuarios': usuarios
        }
        return render(request, template_name, context)
    

@login_required
def ver_direccion(request, direccion_id: int):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error')
        return redirect('login')

    if profile.group_id not in [1, 2]:
        return redirect('logout')

    direccion = get_object_or_404(
        Direccion.objects.select_related('usuario'),
        pk=direccion_id
    )
    return render(request, 'direccion/ver_direccion.html', {'direccion': direccion})

@login_required
def bloquear_direccion(request, pk):
    try:
        profile = Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO, 'Error')
        return redirect('login')

    if profile.group_id == 1:  
        direccion = get_object_or_404(Direccion, pk=pk)
        if direccion.state == "Activo":
            direccion.state = "Inactivo"
            messages.add_message(request, messages.SUCCESS, f"La dirección {direccion.nombre_direccion} fue bloqueada.")
        else:
            direccion.state = "Activo"
            messages.add_message(request, messages.SUCCESS, f"La dirección {direccion.nombre_direccion} fue activada.")
        direccion.save()
        return redirect('gestion_direccion')
    else:
        return redirect('logout')
    
    
@login_required
def departamento_e_incidencia_asociadas(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.error(request, 'Error al obtener el perfil.')
        return redirect('login')

    if profile.group_id == 2:
        direccion = Direccion.objects.filter(usuario=request.user).first()
        if not direccion:
            messages.info(request, 'No tienes una dirección asignada.')
            return redirect('main_direccion')

        qs = (
            Departamento.objects.filter(direccion=direccion)
            .select_related('usuario', 'direccion')
            .order_by('id')
        )

        paginator = Paginator(qs, 6)  
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            'direccion/departamento_e_incidencia_asociadas.html',
            {
                'direccion': direccion,
                'departamentos': page_obj,   
                'page_obj': page_obj
            }
        )

    else:
        return redirect('logout')




@login_required
def incidencias_direccion(request):
    try:

        direccion_usuario = Direccion.objects.get(usuario=request.user)


        departamentos = Departamento.objects.filter(direccion=direccion_usuario)


        estado_filtro = request.GET.get("estado", "Todos")

 
        incidencias_asociadas = Incidencia.objects.filter(departamento__in=departamentos)


        if estado_filtro != "Todos":
            incidencias_asociadas = incidencias_asociadas.filter(estado=estado_filtro)


        paginator = Paginator(incidencias_asociadas, 6)  # 10 incidencias por página
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            'direccion': direccion_usuario,
            'departamentos': departamentos,
            'incidencias': page_obj,          
            'estado_actual': estado_filtro,   
        }

        return render(request, 'direccion/incidencias_direccion.html', context)

    except Direccion.DoesNotExist:
        messages.error(request, 'No estás asignado a ninguna dirección.')
        return redirect('main_direccion')
