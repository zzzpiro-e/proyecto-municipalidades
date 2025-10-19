from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from registration.models import Profile
from departamento.models import Departamento
from direccion.models import Direccion
from django.contrib.auth.models import User


@login_required
def main_departamento(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error')
        return redirect('login')

    if profile.group_id ==3:
        departamentos = (Departamento.objects.select_related('usuario', 'direccion').order_by('id'))
        return render(request, 'departamento/main_departamento.html',{'departamentos': departamentos})
    else:
        return redirect('logout')

@login_required
def gestion_departamento(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error')
        return redirect('login')

    if profile.group_id ==1:
        departamentos = (Departamento.objects.select_related('usuario', 'direccion').order_by('id'))
        return render(request, 'departamento/gestion_departamento.html',{'departamentos': departamentos})
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
        usuarios=User.objects.filter(profile__group__id=3,departamento__isnull=True)
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
            return redirect('main_departamento')
        else:
            messages.add_message(request,messages.INFO,'No se pudo realizar la solicitud, intente nuevamente')
            return redirect('check_group_main')
    else:
        return redirect('logout')

@login_required
def ver_departamento(request, departamento_id: int):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error')
        return redirect('login')

    if profile.group_id not in [1, 3]:
        return redirect('logout')
    
    departamento = get_object_or_404(
        Departamento.objects.select_related('usuario', 'direccion'),
        pk=departamento_id
    )
    return render(request, 'departamento/ver_departamento.html', {'departamentos': departamento})




@login_required
def editar_departamento(request, departamento_id=None):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')
    if profile.group_id == 1:
        if request.method == 'POST':
            depto_id = request.POST.get('departamento_id')
            nombre_departamento = request.POST.get('nombre_departamento')
            direccion_id = request.POST.get('direccion')
            usuario_id = request.POST.get("usuario")
            departamento_a_actualizar = get_object_or_404(Departamento, id=depto_id)
            departamento_a_actualizar.nombre_departamento = nombre_departamento
            departamento_a_actualizar.direccion_id = direccion_id
            departamento_a_actualizar.usuario_id = usuario_id
            departamento_a_actualizar.save()
            messages.add_message(request, messages.INFO, 'Departamento actualizado con éxito.')
            return redirect('main_departamento')
        else:
            departamento_para_editar = get_object_or_404(Departamento, id=departamento_id)
            direcciones = Direccion.objects.all()
            usuarios = User.objects.filter(profile__group__id=3)
            template_name = 'departamento/editar_departamento.html'
            context = {
                'departamento': departamento_para_editar,
                'direcciones': direcciones,
                'usuarios': usuarios
            }
            return render(request, template_name, context)
    else:
        return redirect('logout')

@login_required
def bloquear_departamento(request, pk):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.error(request, 'Error')
        return redirect('login')

    if profile.group_id == 1:
        departamento = get_object_or_404(Departamento, id=pk)
        if departamento.state == 'Activo':
            departamento.state = 'Bloqueado'
            messages.success(request, f"Departamento {departamento.nombre_departamento} bloqueado")
        else:
            departamento.state = 'Activo'
            messages.success(request, f"Departamento {departamento.nombre_departamento} activado")
        departamento.save()
        return redirect('main_departamento')
    return redirect('logout')

@login_required
def ver_departamento_bloqueo(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.error(request, 'Error')
        return redirect('login')

    if profile.group_id == 1:
        departamentos = Departamento.objects.filter(state='Bloqueado').select_related('usuario','direccion')
        return render(request, 'departamento/bloquear_departamento.html', {'departamentos': departamentos})
    return redirect('logout')