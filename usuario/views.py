from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from registration.models import Profile
from django.contrib.auth.models import User, Group
from core.models import Usuario
from territorial.models import Territorial

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
        profile = Profile.objects.get(user_id=request.user.id)
    except:
        messages.error(request, "Error")
        return redirect('check_profile')

    if profile.group_id == 1:
        if request.method == 'POST':

            username = request.POST.get('username')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            group_id = request.POST.get('group_id')
            zona = request.POST.get('zona')  # <-- zona como texto

            if username=='' or password=='' or first_name=='' or last_name=='' or email=='' or not group_id:
                messages.info(request, 'Debes ingresar toda la información')
                return redirect('crear_usuario')

            # Crear usuario
            usuario_save = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email
            )

            # Crear perfil
            perfil_save = Profile.objects.create(
                user=usuario_save,
                group_id=group_id
            )

            # Si es territorial, crea Territorial con zona charfield
            group_obj = Group.objects.get(id=group_id)
            if group_obj.name == "Territorial":
                
                if not zona:
                    messages.error(request, "Debe ingresar zona para usuarios territoriales.")
                    return redirect("crear_usuario")

                Territorial.objects.create(
                    usuario=usuario_save,
                    zona_asignada=zona   # <-- zona es texto
                )

            messages.success(request, "Usuario creado con éxito")
            return redirect('main_usuario')

        messages.error(request, "Solicitud inválida")
        return redirect('check_group_main')

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

