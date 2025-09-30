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
    if profile.group_id in [1,3]:
        template_name = 'departamento/main_departamento.html'
        return render(request,template_name)
    else: 
        return redirect('logout')

    
