from django.contrib import admin
from .models import *

class HistorialGestionAdmin(admin.ModelAdmin):
    list_display = ('activo', 'fecha_evento', 'mmt_tipo', 'detalle_evento', 'responsable')
    search_fields = ('activo__codigo', 'detalle_evento', 'responsable')
    list_filter = ('mmt_tipo', 'fecha_evento', 'responsable')


admin.site.register(HistorialGestion, HistorialGestionAdmin)