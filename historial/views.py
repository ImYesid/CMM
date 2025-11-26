from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import HistorialGestion

@login_required(login_url='login')
def trazabilidad_historial(request):
    historial = HistorialGestion.objects.select_related('activo').order_by('-fecha_evento')

    tipo_filtro = request.GET.get('tipo')
    activo_filtro = request.GET.get('activo')

    if tipo_filtro:
        historial = historial.filter(mmt_tipo=tipo_filtro)
    if activo_filtro:
        historial = historial.filter(activo__codigo__icontains=activo_filtro)

    return render(request, 'historial/historial.html', {
        'historial': historial,
        'tipos': HistorialGestion.MMT_TIPO_CHOICES,
    })
