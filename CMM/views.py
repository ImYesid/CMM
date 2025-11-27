from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from orden_trabajo.models import OrdenTrabajo
from incidencia.models import Incidencia
from activos.models import Activo
from django.db.models import Count
from usuarios.models import PerfilUsuario

@login_required(login_url='login')
def home(request):
    perfil = request.user.perfilusuario     # <- tu perfil
    rol = perfil.cargo.cargo 
    return render(request, 'home.html', {'mensaje': 'Bienvenido a la página principal'
                                         , 'role':rol})

def dashboard_data(request):
    User = get_user_model()

    operarios_activos = User.objects.filter(
        perfilusuario__cargo__cargo="Tecnico",
        is_active=True
    ).count()
    activos_operativos = Activo.objects.filter(estado_operativo__iexact="operativo").count()
    total_incidencias = Incidencia.objects.count()
    activos_totales = Activo.objects.count()
    indice_incidencias = round((total_incidencias / activos_totales) * 100, 2) if activos_totales else 0
    ot_por_estado = OrdenTrabajo.objects.values('OT_estado').annotate(total=Count('id'))

    return JsonResponse({
        "operarios_activos": operarios_activos,
        "activos_operativos": activos_operativos,
        "indice_incidencias": indice_incidencias,
        "ot_estado_proceso": list(ot_por_estado)
    })