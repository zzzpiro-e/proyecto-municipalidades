from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from registration.models import Profile
from .models import Territorial
from django.contrib.auth.models import User
from django.core.paginator import Paginator

@login_required
def main_territorial(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error de perfil.')
        return redirect('login')

    if profile.group_id in [4]:
        territoriales = (Territorial.objects.select_related('usuario').order_by('id'))
        return render(
            request,
            'territorial/main_territorial.html',{'territoriales': territoriales}
        )
    return redirect('logout')


@login_required
def gestion_territorial(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error de perfil.')
        return redirect('login')

    if profile.group_id == 1:
        qs = Territorial.objects.select_related('usuario').order_by('id')

        paginator = Paginator(qs, 6)  
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            'territorial/gestion_territorial.html',
            {
                'territoriales': page_obj,
                'page_obj': page_obj
            }
        )

    return redirect('logout')


@login_required
def editar_territorial(request, territorial_id=None):
    try:
        profile = Profile.objects.filter(user_id=request.user.id).get()
    except:
        messages.add_message(request, messages.INFO, 'Error de perfil')
        return redirect('login')
    if profile.group_id == 1:
        if request.method == 'POST':
            terr_id = request.POST.get('territorial_id')
            usuario_id = request.POST.get("usuario")
            zona_asignada = request.POST.get('zona_asignada')
            observaciones = request.POST.get('observaciones')
            territorial_a_actualizar = get_object_or_404(Territorial, id=terr_id)
            territorial_a_actualizar.usuario_id = usuario_id
            territorial_a_actualizar.zona_asignada = zona_asignada
            territorial_a_actualizar.observaciones = observaciones
            territorial_a_actualizar.save()
            messages.add_message(request, messages.INFO, 'Territorial actualizado con éxito.')
            return redirect('main_territorial')
        else:
            territorial = get_object_or_404(Territorial, id=territorial_id)
            usuarios = User.objects.filter(profile__group__id=4)
            template_name = 'territorial/editar_territorial.html'
            context = {
                'territorial': territorial,
                'usuarios': usuarios
            }
            return render(request, template_name, context)
    else:
        return redirect('logout')

@login_required
def ver_territorial(request, territorial_id: int):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.info(request, 'Error de perfil')
        return redirect('login')

    if profile.group_id not in [1, 4]:
        return redirect('logout')

    territorial = get_object_or_404(
        Territorial.objects.select_related('usuario'),pk=territorial_id
    )
    return render(
        request,
        'territorial/ver_territorial.html',{'territorial': territorial}
    )

    
@login_required
def lista_editar_territorial(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error de perfil.')
        return redirect('login')
    if profile.group_id == 1:
        territoriales = Territorial.objects.all()
        context = {'territoriales': territoriales}
        return render(request, 'territorial/lista_editar_territorial.html', context)
    else:
        return redirect('logout')
    

@login_required
def bloquear_territorial(request, pk):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        messages.error(request, 'Error de perfil')
        return redirect('login')

    if profile.group_id == 1:
        territorial = get_object_or_404(Territorial, id=pk)
        if territorial.state == 'Activo':
            territorial.state = 'Bloqueado'
            messages.success(request, f"Territorial {territorial.zona_asignada} bloqueado correctamente")
        else:
            territorial.state = 'Activo'
            messages.success(request, f"Territorial {territorial.zona_asignada} activado correctamente")
        territorial.save()
        return redirect('main_territorial')
    else:
        return redirect('logout')
