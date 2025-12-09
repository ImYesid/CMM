from usuarios.models import PerfilUsuario
from orden_trabajo.models import NotificacionOT

def global_context(request):
    user = None
    perfil = None
    notificaciones = []

    if request.user.is_authenticated:
        user = request.user
        perfil = PerfilUsuario.objects.filter(usuario=request.user).first()
        # Filtrar OT cerradas con encuesta incompleta
        notificaciones = NotificacionOT.objects.filter(
            usuario=user,
            orden_trabajo__OT_estado="cerrada",
            orden_trabajo__encuesta=False,
            leida=False
        ).order_by('-fecha_creacion')

    return {
        'perfil': perfil,
        'user': user,
        'notificaciones' : notificaciones,
    }