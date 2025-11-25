from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import *
from .forms import *


@login_required(login_url = 'login')
def plan_gestion(request):
    planes_preventivos = PlanGestion.objects.filter(plan_tipo="preventivo")

    context = {
        'planes_preventivos': planes_preventivos,
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