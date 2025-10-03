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
        profile= Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request,messages.INFO, 'Error')
        return redirect('login')
    if profile.group_id ==5:
        template_name = 'cuadrilla/main_cuadrilla.html'
        return render(request,template_name)
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
            return redirect('gestion_cuadrilla')
        else:
            messages.add_message(request,messages.INFO,'No se pudo realizar la solicitud, intente nuevamente')
            return redirect('check_group_main')
    else:
        return redirect('logout')