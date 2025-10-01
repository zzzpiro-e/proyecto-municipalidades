from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect
from registration.models import Profile
@login_required

def main_direccion(request):
    try:
        profile= Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request,messages.INFO, 'Error')
        return redirect('login')
    if profile.group_id in [1,2]:
        template_name = 'direccion/main_direccion.html'
        return render(request,template_name)
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
        return render(request,template_name)
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
            nombre_encargado=request.POST.get('nombre_encargado')
            correo_encargado=request.POST.get('correo_encargado')
            if nombre_direccion=='' or nombre_encargado=='' or correo_encargado=='':
                messages.add_message(request,messages.INFO, 'Debes ingresar toda la información, no pueden quedar campos vacíos')
                return redirect('crear_direccion')
            direccion_save=Direccion(
                nombre_direccion=nombre_direccion,
                nombre_encargado=nombre_encargado,
                correo_encargado=correo_encargado,
                )
            direccion_save.save()
            messages.add_message(request,messages.INFO,'Dirección creada con exito')
            return redirect('gestion_direccion')
        else:
            messages.add_message(request,messages.INFO,'No se pudo realizar la solicitud, intente nuevamente')
            return redirect('check_group_main')
    else:
        return redirect('logout')



