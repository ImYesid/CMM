from usuarios.models import PerfilUsuario

def global_context(request):
    user = None
    perfil = None

    if request.user.is_authenticated:
        user = request.user
        perfil = PerfilUsuario.objects.filter(usuario=request.user).first()

    return {
        'perfil': perfil,
        'user': user,
    }