from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from orden_trabajo.models import OrdenTrabajo
from incidencia.models import Incidencia
from activos.models import Activo
from plan_gestion.models import PlanGestion
from django.db.models import Count, Q
from usuarios.models import PerfilUsuario

@login_required(login_url='login')
def home(request):
    try:
        perfil = request.user.perfilusuario
        rol = perfil.cargo.cargo
    except PerfilUsuario.DoesNotExist:
        messages.error(request, "Tu perfil no está configurado. Contacta al administrador.")
        logout(request)
        return redirect('login')
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
    ot_por_tecnico = (
        User.objects.filter(perfilusuario__cargo__cargo="Tecnico", is_active=True)
        .annotate(
            abiertas=Count('ordenes_asignadas', filter=Q(ordenes_asignadas__OT_estado="abierta")),
            en_ejecucion=Count('ordenes_asignadas', filter=Q(ordenes_asignadas__OT_estado="en_ejecucion"))
        )
        .values('username', 'abiertas', 'en_ejecucion')
    )
    plan_por_tipo = (
        PlanGestion.objects.values('plan_tipo')
        .annotate(total=Count('id'))
    )

    return JsonResponse({
        "operarios_activos": operarios_activos,
        "activos_operativos": activos_operativos,
        "indice_incidencias": indice_incidencias,
        "ot_estado_proceso": list(ot_por_estado),
        "ot_por_tecnico": list(ot_por_tecnico),
        "plan_por_tipo": list(plan_por_tipo)
    })