from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect
from registration.models import Profile
from django.contrib.auth.models import User, Group
from registration.models import Profile
@login_required
#sex
def main_usuario(request):
    try:
        profile= Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request,messages.INFO, 'Error')
        return redirect('login')
    if profile.group_id==1:
        template_name = 'usuario/main_usuario.html'
        return render(request,template_name)
    else: 
        return redirect('logout')

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
            return redirect('gestion_usuario')
        else:
            messages.add_message(request,messages.INFO,'No se pudo realizar la solicitud, intente nuevamente')
            return redirect('check_group_main')
    else:
        return redirect('logout')


