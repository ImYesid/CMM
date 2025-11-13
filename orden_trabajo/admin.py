from django.contrib import admin
from .models import *

class OrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = ('id_OT', 'activo', 'plan', 'descripcion_falla', 'acciones', 'fecha_inicio', 'fecha_fin', 'OT_estado', 'recursos_usados', 'tiempo_intervencion', 'usuario',)
    search_fields = ('activo', 'plan', 'fecha_inicio', 'fecha_fin', 'OT_estado', 'usuario',)
    list_filter = ('activo','fecha_inicio', 'fecha_fin', 'OT_estado',)


admin.site.register(OrdenTrabajo, OrdenTrabajoAdmin)