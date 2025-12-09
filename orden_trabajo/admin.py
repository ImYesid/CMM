from django.contrib import admin
from .models import *

@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'activo', 'plan', 'descripcion_falla', 'acciones', 'fecha_inicio', 'fecha_fin', 'OT_estado', 'recursos_usados', 'tiempo_intervencion', 'usuario', 'tecnico_asignado', 'encuesta',)
    search_fields = ('codigo', 'activo', 'plan', 'fecha_inicio', 'fecha_fin', 'OT_estado', 'usuario', 'tecnico_asignado',)
    list_filter = ('codigo', 'activo','fecha_inicio', 'fecha_fin', 'OT_estado',)

@admin.register(NotificacionOT)
class NotificacionOTAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'orden_trabajo', 'mensaje', 'fecha_creacion', 'leida',)
    search_fields = ('usuario', 'orden_trabajo', 'leida',)
    list_filter = ('usuario', 'orden_trabajo','fecha_creacion', 'leida',)

