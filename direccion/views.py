from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from registration.models import Profile
from direccion.models import Direccion
from django.contrib.auth.models import User
@login_required
<<<<<<< Updated upstream

def main_direccion(request):
=======
def main_direccion(request, direccion_id=None):
>>>>>>> Stashed changes
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error')
        return redirect('login')

    if profile.group_id in [1, 2]:
        direccion_listado = Direccion.objects.select_related('usuario').order_by('id')
        template_name = 'direccion/main_direccion.html'
        return render(request, template_name, {'direcciones': direccion_listado})
    else:
        return redirect('logout')

@login_required
def crear_direccion(request):
    try:
        profile= Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request,messages.INFO, 'Error')
        return redirect('login')
    if profile.group_id ==1:
        template_name = 'direccion/crear_direccion.html'
        usuarios=User.objects.filter(profile__group__id=2)
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
        profile = Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO, 'Error de perfil')
        return redirect('login')
    if profile.group_id == 1:
        if request.method == 'POST':
            dir_id = request.POST.get('direccion_id')
            nombre_direccion = request.POST.get('nombre_direccion')
            usuario_id = request.POST.get("usuario")
            if not nombre_direccion or not usuario_id:
                messages.add_message(request, messages.INFO, 'No pueden quedar campos vacíos.')
                return redirect('editar_direccion', direccion_id=dir_id)
            direccion_a_actualizar = get_object_or_404(Direccion, id=dir_id)
            direccion_a_actualizar.nombre_direccion = nombre_direccion
            direccion_a_actualizar.usuario_id = usuario_id
            direccion_a_actualizar.save()
            messages.add_message(request, messages.INFO, 'Dirección actualizada con éxito.')
            return redirect('editar_direccion', direccion_id=dir_id)
        else:
            direccion = get_object_or_404(Direccion, id=direccion_id)
            usuarios = User.objects.filter(profile__group__id=2)
            template_name = 'direccion/editar_direccion.html'
            context = {
                'direccion': direccion,
                'usuarios': usuarios
            }
            return render(request, template_name, context)
    else:
        return redirect('logout')
    
@login_required
def direccion_ver(request,direccion_id=None):
    try:
<<<<<<< Updated upstream
        profile = Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO, 'Hubo un error')
        return redirect('logout')
    if profile.group_id == 1:
        try:
            direccion_count=Direccion.objects.filter(pk=direccion_id).count()
            if direccion_count<=0:
                messages.add_message(request,messages.INFO,'Hubo un error')
                return redirect('gestion_direccion')
            direccion_data = Direccion.objects.get(pk=direccion_id)
        except:
            messages.add_message(request,messages.INFO,'Hubo un error')
            return redirect('gestion_direccion')
        template_name = 'direccion/ver_direccion.html'
        return render(request,template_name,{'direccion_data':direccion_data})
    else:
        return redirect('logout')
=======
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

    return render(request, 'direccion/ver_direccion.html', {
        'direccion': direccion
    })

>>>>>>> Stashed changes
