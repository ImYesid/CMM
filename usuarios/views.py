from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import Usuario, ConfiguracionUsuario
from .forms import LoginForm
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from usuarios.models import PerfilUsuario

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            remember_me = request.POST.get('remember_me')

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)

                if not remember_me:  
                    request.session.set_expiry(0)  # Sesión expira al cerrar navegador
                else:
                    request.session.set_expiry(1209600)  # 2 semanas de sesión activa

                messages.success(request, 'Ha Iniciado Sesión Con Éxito')
                return redirect('home')
            else:
                messages.error(request, 'Credenciales de acceso invalidos')
                return redirect('login')
        else:
            form = LoginForm()  
            return render(request, 'usuarios/login.html', {'form' : form})

        
@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email') 
        user = Usuario.objects.filter(email=email).first()  

        if user:
            # Configurar el email de restablecimiento de contraseña
            current_site = get_current_site(request)
            mail_subject = 'Restablecer su contraseña'
            message = render_to_string('usuarios/reset-password-email.html', {
                'user': user,
                'domain': current_site.domain,  # Agrega .domain para obtener la URL
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            # Enviar el email
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()

            messages.success(request, 'Se ha enviado un correo electrónico de restablecimiento de contraseña.')
            return redirect('login')
        else:
            messages.error(request, '¡La cuenta no existe!')
            return redirect('forgot_password')

    form = LoginForm() 
    return render(request, 'usuarios/forgot-password.html', {'form' : form})

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # Decodificar UID
        user = Usuario.objects.filter(pk=uid).first()  # Obtener usuario o None
    except (TypeError, ValueError, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        request.session['uid'] = uid  # Guardar UID en sesión para resetear la contraseña
        messages.success(request, 'Por favor, restablezca su contraseña.')
        return redirect('reset_password')
    else:
        messages.error(request, '¡Este enlace ha expirado o es inválido!')
        return redirect('forgot_password')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password'].strip()
        confirm_password = request.POST['confirm_password'].strip()

        if password != confirm_password:
            messages.error(request, '¡Las contraseñas no coinciden!')
            return redirect('reset_password')

        uid = request.session.get('uid')
        if not uid:
            messages.error(request, '¡La sesión ha expirado! Intente nuevamente.')
            return redirect('forgot_password')

        user = Usuario.objects.filter(pk=uid).first()
        if not user:
            messages.error(request, '¡Usuario no encontrado!')
            return redirect('forgot_password')

        # Validar seguridad de la contraseña
        try:
            validate_password(password, user)
        except ValidationError as e:
            messages.error(request, '. '.join(e.messages))
            return redirect('reset_password')

        # Guardar la nueva contraseña
        user.set_password(password)
        user.save()

        # Mantener la sesión activa después del cambio de contraseña
        update_session_auth_hash(request, user)

        # Eliminar el uid de la sesión
        del request.session['uid']

        messages.success(request, 'Restablecimiento de contraseña exitoso')
        return redirect('login')

    return render(request, 'usuarios/reset-password.html')

@login_required
def theme_settings(request):
    usuario = request.user  
    configuracion, created = ConfiguracionUsuario.objects.get_or_create(usuario=usuario)

    if request.method == 'POST':
        configuracion.tema = request.POST.get('tema', configuracion.tema)
        configuracion.color_encabezado = request.POST.get('color_encabezado', configuracion.color_encabezado)
        configuracion.color_sidebar = request.POST.get('color_sidebar', configuracion.color_sidebar)
        configuracion.save()
        return redirect('home')  # Cambia esto a la vista que prefieras después de actualizar

    return render(request, 'includes/switcher.html', {'configuracion': configuracion})          

@login_required
def update_profile(request):
    if request.method == "POST":
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        
        
        perfil = PerfilUsuario.objects.filter(usuario=request.user).first()
        if perfil:
            perfil.telefono = telefono
            perfil.save()
        
        user = request.user
        user.email = email
        user.save()

        messages.success(request, "Perfil actualizado exitosamente.")
        return redirect('profile')
    
    messages.error(request, "Hubo un error al actualizar el perfil.")
    return render(request, 'profile.html')