from django.contrib import admin
from .models import *

class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ('activo', 'descripcion', 'fecha_reporte', 'nivel_prioridad', 'estado', 'usuario',)
    search_fields = ('activo', 'descripcion', 'fecha_reporte', 'nivel_prioridad', 'estado', 'usuario',)
    list_filter = ('activo','fecha_reporte','usuario',)


admin.site.register(Incidencia, IncidenciaAdmin)