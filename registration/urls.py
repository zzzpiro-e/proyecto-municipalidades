from django.urls import path
from .views import SignUpView, ProfileUpdate, EmailUpdate, password_reset_request, profile_edit
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('profile/', ProfileUpdate.as_view(), name="profile"),  
    path('profile/email/', EmailUpdate.as_view(), name="profile_email"),       
    path('profile_edit/', profile_edit, name='profile_edit'),    
    
    # Restablecimiento de contraseña
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),

    # Confirmación de envío de correo
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # Formulario para cambiar contraseña (desde el link del correo)
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    # Contraseña cambiada con éxito
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    ]
