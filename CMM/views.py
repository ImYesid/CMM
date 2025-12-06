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
import locale
from datetime import datetime

@login_required(login_url='login')
def home(request):
    try:
        perfil = request.user.perfilusuario
    except PerfilUsuario.DoesNotExist:
        messages.error(request, "Tu perfil no está configurado. Contacta al administrador.")
        logout(request)
        return redirect('login')
    return render(request, 'home.html', {'mensaje': 'Bienvenido a la página principal'})

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

    #Calcular MTBF, MTTR y Disponibilidad por mes
    mtbf_por_mes, mttr_por_mes = {}, {}

    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'spanish')
        except locale.Error:
            locale.setlocale(locale.LC_TIME, '')


    for activo in Activo.objects.all():
        ots = OrdenTrabajo.objects.filter(activo=activo).order_by('fecha_inicio')
        if ots.count() > 1:
            fechas = list(ots.values_list('fecha_inicio', flat=True))
            # MTBF: intervalos entre OT consecutivas
            for i in range(1, len(fechas)):
                delta = fechas[i] - fechas[i-1]
                horas = delta.total_seconds() / 3600
                fecha = fechas[i]
                clave = f"{fecha.year}-{fecha.month:02d}"
                nom_mes = fecha.strftime("%b").capitalize() + f"-{fecha.year}"
                mtbf_por_mes.setdefault(clave, {"nombre": nom_mes, "valores": []})["valores"].append(horas)

        # MTTR: diferencia entre inicio y fin de cada OT cerrada
        for ot in ots.filter(OT_estado="cerrada", fecha_fin__isnull=False):
            delta = ot.fecha_fin - ot.fecha_inicio
            horas = delta.total_seconds() / 3600
            clave = f"{ot.fecha_inicio.year}-{ot.fecha_inicio.month:02d}"
            nom_mes = ot.fecha_inicio.strftime("%b").capitalize() + f"-{ot.fecha_inicio.year}"
            mttr_por_mes.setdefault(clave, {"nombre": nom_mes, "valores": []})["valores"].append(horas)

    # Promedios globales por mes
    indicadores = []
    meses = sorted(set(mtbf_por_mes.keys()) | set(mttr_por_mes.keys()))
    for clave in meses:
        nom_mes = mtbf_por_mes.get(clave, mttr_por_mes.get(clave))["nombre"]
        mtbf = round(sum(mtbf_por_mes.get(clave, {"valores": []})["valores"]) /
                     len(mtbf_por_mes.get(clave, {"valores": []})["valores"]), 2) if mtbf_por_mes.get(clave) else 0
        mttr = round(sum(mttr_por_mes.get(clave, {"valores": []})["valores"]) /
                     len(mttr_por_mes.get(clave, {"valores": []})["valores"]), 2) if mttr_por_mes.get(clave) else 0
        disponibilidad = round(mtbf / (mtbf + mttr), 2) if (mtbf + mttr) > 0 else 0
        indicadores.append({"mes": nom_mes, "mtbf": mtbf, "mttr": mttr, "disponibilidad": disponibilidad})

    # Después de calcular 'indicadores'
    ultimo_mes = indicadores[-1] if indicadores else {"mtbf": 0, "mttr": 0, "disponibilidad": 0}
                            
    return JsonResponse({
        "operarios_activos": operarios_activos,
        "activos_operativos": activos_operativos,
        "indice_incidencias": indice_incidencias,
        "ot_estado_proceso": list(ot_por_estado),
        "ot_por_tecnico": list(ot_por_tecnico),
        "plan_por_tipo": list(plan_por_tipo),
        "indicadores": indicadores,
        "ultimo_mes": ultimo_mes
    })