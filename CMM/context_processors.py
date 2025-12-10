from django.contrib.auth.decorators import login_required
from usuarios.models import PerfilUsuario
from orden_trabajo.models import NotificacionOT

@login_required
def global_context(request):
    user = None
    perfil = None
    notificacionesFiltro = []
    notificaciones = []
    noti_count = []
    filtro = 'all'

    if request.user.is_authenticated:
        user = request.user
        perfil = PerfilUsuario.objects.filter(usuario=request.user).first()

        filtro = request.GET.get('filtro', 'all') 

        if filtro == 'all':
            notificacionesFiltro = NotificacionOT.objects.filter(
                usuario=user,
                orden_trabajo__OT_estado="cerrada"
            ).order_by('-fecha_creacion')
        else:
            notificacionesFiltro = NotificacionOT.objects.filter(
                usuario=user,
                orden_trabajo__OT_estado="cerrada",
                orden_trabajo__encuesta=False,

            ).order_by('-fecha_creacion')

        # Filtrar OT cerradas con encuesta incompleta
        notificaciones = NotificacionOT.objects.filter(
            usuario=user,
            orden_trabajo__OT_estado="cerrada",
            orden_trabajo__encuesta=False,

        ).order_by('-fecha_creacion')

        noti_count = NotificacionOT.objects.filter(
            usuario=user,
            orden_trabajo__OT_estado="cerrada",
            orden_trabajo__encuesta=False,
            leida=False
        ).order_by('-fecha_creacion')

    return {
        'perfil': perfil,
        'user': user,
        'notificacionesFiltro' : notificacionesFiltro,
        'notificaciones' : notificaciones,
        'noti_count' : noti_count,
        'filtro': filtro,
    }