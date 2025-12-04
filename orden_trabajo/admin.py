from django.contrib import admin
from .models import *

class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'activo', 'plan', 'descripcion_falla', 'acciones', 'fecha_inicio', 'fecha_fin', 'OT_estado', 'recursos_usados', 'tiempo_intervencion', 'usuario', 'tecnico_asignado', 'encuesta',)
    search_fields = ('codigo', 'activo', 'plan', 'fecha_inicio', 'fecha_fin', 'OT_estado', 'usuario', 'tecnico_asignado',)
    list_filter = ('codigo', 'activo','fecha_inicio', 'fecha_fin', 'OT_estado',)


admin.site.register(OrdenTrabajo, OrdenTrabajoAdmin)