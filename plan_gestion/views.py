from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from historial.models import HistorialGestion
from orden_trabajo.models import OrdenTrabajo
from django.utils import timezone
from .models import *
from .forms import *

@login_required(login_url = 'login')
def plan_gestion(request, tab_id):
    planes_preventivos = PlanGestion.objects.filter(plan_tipo="preventivo")
    planes_predictivos = PlanGestion.objects.filter(plan_tipo="predictivo")
    planes_correctivos = PlanGestion.objects.filter(plan_tipo="correctivo")
    planes_inspeccion = PlanGestion.objects.filter(plan_tipo="inspeccion")

    forms_por_tipo = {
        'Preventivo': PlanGestionForm(plan_tipo_fijo='preventivo'),
        'Predictivo': PlanGestionForm(plan_tipo_fijo='predictivo'),
        'Correctivo': PlanGestionForm(plan_tipo_fijo='correctivo'),
        'Inspeccion': PlanGestionForm(plan_tipo_fijo='inspeccion'),
    }

    context = {
        'tab_id': tab_id,
        'forms_por_tipo' : forms_por_tipo,
        'planes_preventivos': planes_preventivos,
        'planes_predictivos': planes_predictivos,
        'planes_correctivos': planes_correctivos,
        'planes_inspeccion': planes_inspeccion,
    }

    return render(request, 'plan_gestion/plan_gestion.html', context )

@login_required(login_url='login')
def agregar_plan_tipo(request, tipo):
    if tipo not in ['Preventivo', 'Predictivo', 'Correctivo', 'Inspeccion']:
        return JsonResponse({"success": False, "message": "Tipo de plan inválido."})

    if request.method == "POST":
        form = PlanGestionForm(request.POST, plan_tipo_fijo=tipo)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": f"Plan {tipo} agregado correctamente."})
        else:
            return JsonResponse({"success": False, "message": "Registro inválido."})

    return JsonResponse({"success": False, "message": "Formato incorrecto."})


@login_required(login_url='login')
def editar_plan_tipo(request, plan_id):
    plan = get_object_or_404(PlanGestion, id=plan_id)
    tipo = plan.plan_tipo

    if request.method == "POST":
        form = PlanGestionForm(request.POST, instance=plan, plan_tipo_fijo=tipo)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": f"Plan {tipo} actualizado correctamente."})
        else:
            return JsonResponse({"success": False, "message": "Actualización inválida."})

    data = {field.name: getattr(plan, field.name) for field in plan._meta.fields if hasattr(plan, field.name)}
    return JsonResponse({"success": True, "data": data})

def agregar_plan_tipo(request, tipo):
    if request.method == "POST":
        form = PlanGestionForm(request.POST, plan_tipo_fijo=tipo)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.save()

            # Crear OT automáticamente con el usuario que genera el plan
            OrdenTrabajo.objects.create(
                activo=plan.activo,
                plan=plan,
                descripcion_falla=f"Generada automáticamente desde el plan {plan.plan_nombre}",
                acciones="Pendiente de ejecución",
                fecha_inicio=timezone.now(),
                OT_estado="abierta",
                usuario=request.user   # ← aquí se asigna el usuario actual
            )

            return JsonResponse({"success": True, "message": "Plan de Gestión y OT creados correctamente"})
        else:
            print(form.errors)  # para depurar
            return JsonResponse({"success": False, "message": "Error en el formulario", "errors": form.errors})
    
    else:
        form = PlanGestionForm(plan_tipo_fijo=tipo.lower())
        return render(request, "plan_gestion/plan_gestion.html", {"form": form, "tipo": tipo})
    
def agregar_historial_plan_trabajo(request, tipo):
    if request.method == "POST":
        form = PlanGestionForm(request.POST, plan_tipo_fijo=tipo)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.plan_tipo = tipo.lower()
            plan.save()

            # Crear Historia automáticamente con el usuario que genera el plan
            HistorialGestion.objects.create(
                activo=plan.activo,
                mmt_tipo='plan',
                referencia_id=plan.id,
                descripcion=f"Se creó el plan {plan.plan_nombre}",
                responsable=request.user
            )

            return JsonResponse({"success": True, "message": "Plan de Gestión y OT creados correctamente"})
        else:
            print(form.errors)  # para depurar
            return JsonResponse({"success": False, "message": "Error en el formulario", "errors": form.errors})
    
    else:
        form = PlanGestionForm(plan_tipo_fijo=tipo.lower())
        return render(request, "plan_gestion/plan_gestion.html", {"form": form, "tipo": tipo})
