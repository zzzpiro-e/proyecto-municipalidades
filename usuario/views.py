from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from registration.models import Profile
from django.contrib.auth.models import User, Group
from core.models import Usuario
from django.db import IntegrityError

@login_required
def main_usuario(request, usuario_id=None):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error')
        return redirect('login')

    if profile.group_id == 1:
        usuarios = (
            User.objects
                .prefetch_related('groups')  
                .order_by('id')
        )
        return render(request, 'usuario/main_usuario.html', {
            'usuarios': usuarios
        })
    else:
        return redirect('logout')
    
@login_required
def ver_usuario(request, user_id= None):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error')
        return redirect('login')
    if profile.group_id != 1:
        return redirect('logout')
    usuario = get_object_or_404(
        User.objects.select_related('profile', 'profile__group'),
        pk=user_id
    )
    return render(request, 'usuario/ver_usuario.html', {
        'usuario': usuario
    })

def crear_usuario(request):
    try:
        profile= Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request,messages.INFO, 'Error')
        return redirect('login')
    if profile.group_id ==1:
        template_name = 'usuario/crear_usuario.html'
        grupos=Group.objects.all()
        return render(request,template_name,{"grupos":grupos})
    else: 
        return redirect('logout')
    
@login_required
def guardar_usuario(request):
    try:
        profile=Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO,"Error")
        return redirect('check_profile')
    if profile.group_id==1:
        if request.method=='POST':
            username=request.POST.get('username')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get("last_name")
            email=request.POST.get("email")
            group_id=request.POST.get('group_id')
            if username=='' or first_name=="" or last_name=="" or email=="" or not group_id:
                messages.add_message(request,messages.INFO, 'Debes ingresar toda la información, no pueden quedar campos vacíos')
                return redirect('crear_usuario')
            try:
                usuario_save=User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=username,
                    email=email
                )
                usuario_save.save()
            except IntegrityError:
                messages.error(request, f'Error: El nombre de usuario "{username}" ya existe.')
                return redirect('crear_usuario')
            perfil_save = Profile(
                user=usuario_save,
                group_id=group_id
            )
            perfil_save.save()
            messages.add_message(request,messages.INFO,'Usuario creado con exito')
            return redirect('main_usuario')
        else:
            messages.add_message(request,messages.INFO,'No se pudo realizar la solicitud, intente nuevamente')
            return redirect('check_group_main')
    else:
        return redirect('logout')

@login_required
def eliminar_usuario(request, usuario_id):
    """
    Elimina únicamente el usuario seleccionado.
    Solo admin puede ejecutar.
    """
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error de perfil')
        return redirect('login')

    if profile.group_id != 1:
        return redirect('logout')

    usuario = get_object_or_404(User, pk=usuario_id)
    usuario.delete()
    messages.success(request, f'Usuario {usuario.username} eliminado con éxito')
    return redirect('main_usuario')

@login_required
def editar_usuario(request, user_id=None):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')

    if profile.group_id != 1:
        return redirect('logout')
    usuario_a_editar = get_object_or_404(User.objects.select_related('profile'), id=user_id)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        is_active = request.POST.get('is_active') == 'on'
        telefono = request.POST.get('telefono')
        group_id = request.POST.get('group')
        usuario_a_editar.first_name = first_name
        usuario_a_editar.last_name = last_name
        usuario_a_editar.email = email
        usuario_a_editar.is_active = is_active
        usuario_a_editar.save()

        if usuario_a_editar.profile:
            usuario_a_editar.profile.telefono = telefono
            usuario_a_editar.profile.group_id = group_id
            usuario_a_editar.profile.save()

        messages.add_message(request, messages.INFO, 'Usuario actualizado con éxito.')
        return redirect('main_usuario')

    else:
        grupos = Group.objects.all()
        template_name = 'usuario/editar_usuario.html'
        context = {
            'usuario': usuario_a_editar,
            'grupos': grupos
        }
        return render(request, template_name, context)