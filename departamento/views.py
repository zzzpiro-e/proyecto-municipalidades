from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect
from registration.models import Profile
@login_required

def main_departamento(request):
    try:
        profile= Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request,messages.INFO, 'Error')
        return redirect('login')
    if profile.group_id ==3:
        template_name = 'departamento/main_departamento.html'
        return render(request,template_name)
    else: 
        return redirect('logout')

def crear_departamento(request):
    try:
        profile= Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request,messages.INFO, 'Error')
        return redirect('login')
    if profile.group_id ==1:
        direcciones=Direccion.objects.all()
        usuarios=User.objects.filter(profile__group__id=3)
        template_name = 'departamento/crear_departamento.html'
        return render(request,template_name,{"direcciones":direcciones,"usuarios":usuarios})
    else: 
        return redirect('logout')


@login_required
def guardar_departamento(request):
    try:
        profile=Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO,"Error")
        return redirect('check_profile')
    if profile.group_id==1:
        if request.method=='POST':
            nombre_departamento=request.POST.get('nombre_departamento')
            direccion_id=request.POST.get('direccion')
            usuario_id=request.POST.get("usuario")

            if nombre_departamento=='' or not direccion_id or not usuario_id:
                messages.add_message(request,messages.INFO, 'Debes ingresar toda la información, no pueden quedar campos vacíos')
                return redirect('crear_departamento')
            departamento_save=Departamento(
                nombre_departamento=nombre_departamento,
                direccion_id=direccion_id,
                usuario_id=usuario_id
                )
            departamento_save.save()
            messages.add_message(request,messages.INFO,'Departamento creado con exito')
            return redirect('gestion_departamento')
        else:
            messages.add_message(request,messages.INFO,'No se pudo realizar la solicitud, intente nuevamente')
            return redirect('check_group_main')
    else:
        return redirect('logout')

    

