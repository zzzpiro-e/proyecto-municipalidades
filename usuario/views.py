from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from registration.models import Profile
from django.contrib.auth.models import User, Group
from registration.models import Profile

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
        User.objects.prefetch_related('groups'),
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
            password=request.POST.get('password')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get("last_name")
            email=request.POST.get("email")
            group_id=request.POST.get('group_id')

            if username=='' or password=="" or first_name=="" or last_name=="" or email=="" or not group_id:
                messages.add_message(request,messages.INFO, 'Debes ingresar toda la información, no pueden quedar campos vacíos')
                return redirect('crear_usuario')
            usuario_save=User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email
              )
            usuario_save.save()
            
            perfil_save = Profile(
            user=usuario_save,
            group_id=group_id
            )
            perfil_save.save()

            messages.add_message(request,messages.INFO,'usuario creado con exito')
            return redirect('main_usuario')
        else:
            messages.add_message(request,messages.INFO,'No se pudo realizar la solicitud, intente nuevamente')
            return redirect('check_group_main')
    else:
        return redirect('logout')





@login_required
def eliminar_usuario_lista(request):
    try:
        profile = Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO, 'Error')
        return redirect('login')

    if profile.group_id == 1:  # Solo admin puede
        usuarios = User.objects.all().exclude(id=request.user.id)  # excluye al usuario logueado
        template_name = 'usuario/eliminar_usuario_lista.html'
        return render(request, template_name, {"usuarios": usuarios})
    else:
        return redirect('logout')


@login_required
def eliminar_usuario(request, usuario_id):
    try:
        profile = Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO, 'Error')
        return redirect('login')

    if profile.group_id == 1:
        try:
            usuario = User.objects.get(id=usuario_id)
            usuario.delete()
            messages.add_message(request, messages.INFO, 'Usuario eliminado con éxito')
        except User.DoesNotExist:
            messages.add_message(request, messages.INFO, 'El usuario no existe')
        return redirect('eliminar_usuario_lista')
    else:
        return redirect('logout')
