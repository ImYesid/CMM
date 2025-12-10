from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from historial.models import HistorialGestion
from .forms import *
from .models import *

@login_required(login_url = 'login')
def orden_trabajo(request):
    filtro = request.GET.get('filtro', 'activos') 

    if filtro == 'activos':
        ordenes = OrdenTrabajo.objects.filter(OT_estado__in=['abierta', 'en_ejecucion'])
    else:
        ordenes = OrdenTrabajo.objects.all()

    context = {
        'ordenes': ordenes,
        'filtro': filtro,
    }
    return render(request, 'orden_trabajo/orden_trabajo.html', context)

@login_required(login_url='login')
def agregar_orden_trabajo(request):

    temp = request.session.pop('incidencia_temp', None)

    if request.method == 'POST':
        form = OrdenTrabajoForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.usuario = request.user  #asigna automáticamente el usuario autenticado
            orden.save()
            #si veniamos desde incidencia
            if request.POST.get('action') == 'Agregar desde Incidencia':
                #se lleva todos los campos llave de la ot
                data = {
                    'OT': orden.id,
                    'activo':orden.activo.id,
                    'descripcion':orden.descripcion_falla,
                    'usuario':orden.usuario.id
                }
                request.session['ot_creada'] = data
                messages.success(request, "OT agregada correctamente.")
                return redirect('agregar_incidencia')
            
            HistorialGestion.objects.create(
                activo=orden.activo,
                mmt_tipo=orden.plan.plan_tipo if orden.plan else 'correctivo',
                referencia_id=orden.id,
                detalle_evento=f"Se creó la OT {orden.codigo}",
                usuario=request.user
            )

            return redirect('orden_trabajo')
    else:
        form = OrdenTrabajoForm(initial=temp) if temp else OrdenTrabajoForm()

    context = {
        'form': form,
        'accion': 'Agregar desde Incidencia' if temp else 'Agregar',
        'now': timezone.now()
    }
        
    return render(request, 'orden_trabajo/forms/form_orden_trabajo.html', context)

@login_required(login_url='login')
def editar_orden_trabajo(request, id_OT):
    ot = get_object_or_404(OrdenTrabajo, id=id_OT)
    
    if request.method == "POST":
        form = OrdenTrabajoForm(request.POST, instance=ot)
        if form.is_valid():
            form.save()
            messages.success(request, "OT actualizada correctamente.")
            return redirect('orden_trabajo')
        else:
            messages.error(request, "Actualizacion invalida.")
    else:
        form = OrdenTrabajoForm(instance=ot)

    context = {
        'form': form,
        'accion': 'Editar',
        'codigo': ot.codigo
    }
    
    return render(request, 'orden_trabajo/forms/form_orden_trabajo.html', context)

#NOTIFICACIONES
@login_required
def marcar_notificacion_leida(request, notificacion_id):
    notificacion = get_object_or_404(NotificacionOT, id=notificacion_id, usuario=request.user)
    notificacion.leida = True
    notificacion.save(update_fields=['leida'])
    return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def marcar_todas_leidas(request):
    NotificacionOT.objects.filter(usuario=request.user, leida=False).update(leida=True)
    return redirect(request.META.get("HTTP_REFERER", "/"))