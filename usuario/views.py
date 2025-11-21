from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from registration.models import Profile
from django.contrib.auth.models import User, Group
from core.models import Usuario
from django.db import IntegrityError
from territorial.models import Territorial
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator


@login_required
def main_usuario(request, usuario_id=None):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error')
        return redirect('login')

    if profile.group_id == 1:
        rol_filtro = request.GET.get("rol", "Todos")
        usuarios_list = (
           User.objects
        .exclude(id=request.user.id)
        .select_related("profile__group")  # trae profile y group
        .order_by("id")
        )
        if rol_filtro != "Todos":
            usuarios_list = usuarios_list.filter(profile__group__name=rol_filtro)
        
        paginator = Paginator(usuarios_list, 6)  
        page_number = request.GET.get('page')
        usuarios = paginator.get_page(page_number)

        context = {
            'usuarios': usuarios,
            'profile': profile,
            'rol_actual': rol_filtro
        }
        return render(request, 'usuario/main_usuario.html',context)
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
        profile = Profile.objects.get(user_id=request.user.id)
    except:
        messages.error(request, "Error de perfil")
        return redirect('check_profile')

    if profile.group_id == 1:
        if request.method == 'POST':
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            group_id = request.POST.get('group_id')
            zona = request.POST.get('zona')
            telefono = request.POST.get('telefono')

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
            except IntegrityError:
                messages.error(request, f'Error: El nombre de usuario "{username}" ya existe.')
                return redirect('crear_usuario')
            
            perfil_save = Profile.objects.create(
                user=usuario_save,
                group_id=group_id,
                telefono=telefono
            )

            group_obj = Group.objects.get(id=group_id)
            if group_obj.name == "Territorial":
                if not zona:
                    messages.error(request, "Debe ingresar zona para usuarios territoriales.")
                    usuario_save.delete() 
                    return redirect("crear_usuario")

                Territorial.objects.create(
                    usuario=usuario_save,
                    zona_asignada=zona 
                )

            messages.success(request, "Usuario creado con éxito")
            return redirect('main_usuario')

        messages.error(request, "Solicitud inválida (no-POST)")
        return redirect('check_profile')

    return redirect('logout')

@login_required
def eliminar_usuario(request, usuario_id):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error de perfil')
        return redirect('login')

    if profile.group_id != 1:
        return redirect('logout')

    usuario = get_object_or_404(User, pk=usuario_id)
    if usuario.id == request.user.id:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('main_usuario')
        
    usuario.delete()
    messages.success(request, f'Usuario {usuario.username} eliminado con éxito')
    return redirect('main_usuario')

@login_required
def editar_usuario(request, user_id=None):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.error(request, "Error de perfil.")
        return redirect('login')
    if profile.group_id != 1:
        return redirect('logout')
    usuario = get_object_or_404(User, id=user_id)
    territorial = Territorial.objects.filter(usuario=usuario).first()

    if request.method == "POST":
        usuario.first_name = request.POST.get("first_name")
        usuario.last_name = request.POST.get("last_name")
        usuario.email = request.POST.get("email")
        usuario.save()
        usuario.profile.telefono = request.POST.get("telefono")
        nuevo_group_id = request.POST.get("group")
        usuario.profile.group_id = nuevo_group_id
        usuario.profile.save()
        if nuevo_group_id == "4":
            zona = request.POST.get("zona_asignada")
            if not territorial:
                territorial = Territorial(usuario=usuario)
            territorial.zona_asignada = zona
            territorial.save()
        else:
            if territorial:
                territorial.delete()

        messages.success(request, "Usuario actualizado correctamente.")
        return redirect("main_usuario")
    else:
        grupos = Group.objects.all()
        context = {
            "usuario": usuario,
            "grupos": grupos,
            "territorial": territorial,
        }
        return render(request, "usuario/editar_usuario.html", context)

    
@login_required
def cambiar_contraseña_obligatorio(request):
    profile = request.user.profile

    if not profile.first_session:
        return redirect('check_profile')

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            profile.first_session = 'No'
            profile.save()
            
            messages.success(request, '¡Contraseña cambiada con éxito! Ya puedes usar el sistema.')
            return redirect('check_profile')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form
    }
    return render(request, 'usuario/cambiar_contraseña_obligatorio.html', context)

@login_required
def ver_perfil(request):
    profile = request.user.profile

    if request.method == "POST":
        request.user.email = request.POST.get("email")
        request.user.save()

        profile.telefono = request.POST.get("telefono")
        profile.save()

        messages.success(request, "Perfil actualizado correctamente.")
        return redirect("ver_perfil")

    return render(request, "usuario/ver_perfil.html")