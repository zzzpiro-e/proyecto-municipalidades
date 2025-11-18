from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from registration.models import Profile
from cuadrilla.models import Cuadrilla
from departamento.models import Departamento
from django.contrib.auth.models import User


@login_required
def main_cuadrilla(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error')
        return redirect('login')

    if profile.group_id in [1,5]:
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

    if profile.group_id ==1:
        cuadrillas = (Cuadrilla.objects.select_related('usuario', 'departamento').order_by('id'))
        return render(request, 'cuadrilla/gestion_cuadrilla.html', {'cuadrillas': cuadrillas})
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
        usuarios=User.objects.filter(profile__group__id=5)
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
            return redirect('main_cuadrilla')
        else:
            messages.add_message(request,messages.INFO,'No se pudo realizar la solicitud, intente nuevamente')
            return redirect('check_group_main')
    else:
        return redirect('logout')

@login_required
def editar_cuadrilla(request, cuadrilla_id=None):
    try:
        profile = Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO, 'Error de perfil')
        return redirect('login')
    if profile.group_id == 1:
        if request.method == 'POST':
            c_id = request.POST.get('cuadrilla_id')
            nombre_cuadrilla = request.POST.get('nombre_cuadrilla')
            tipo = request.POST.get('tipo')
            departamento_id = request.POST.get('departamento')
            usuario_id = request.POST.get("usuario")
            if not all([nombre_cuadrilla, tipo, departamento_id, usuario_id]):
                messages.add_message(request, messages.INFO, 'No pueden quedar campos vacíos.')
                return redirect('editar_cuadrilla', cuadrilla_id=c_id)
            cuadrilla_a_actualizar = get_object_or_404(Cuadrilla, id=c_id)
            cuadrilla_a_actualizar.nombre_cuadrilla = nombre_cuadrilla
            cuadrilla_a_actualizar.tipo = tipo
            cuadrilla_a_actualizar.departamento_id = departamento_id
            cuadrilla_a_actualizar.usuario_id = usuario_id
            cuadrilla_a_actualizar.save()
            messages.add_message(request, messages.INFO, 'Cuadrilla actualizada con éxito.')
            return redirect('main_cuadrilla')
        else:
            cuadrilla = get_object_or_404(Cuadrilla, id=cuadrilla_id)
            departamentos = Departamento.objects.all()
            usuarios = User.objects.filter(profile__group__id=5)
            template_name = 'cuadrilla/editar_cuadrilla.html'
            context = {
                'cuadrilla': cuadrilla,
                'departamentos': departamentos,
                'usuarios': usuarios
            }
            return render(request, template_name, context)
    else:
        return redirect('logout')

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
        return redirect('main_cuadrilla')
    else:
        return redirect('logout')

