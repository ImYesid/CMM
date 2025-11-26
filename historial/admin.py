from django.contrib import admin
from .models import *

class HistorialGestionAdmin(admin.ModelAdmin):
    list_display = ('activo', 'fecha_evento', 'mmt_tipo', 'detalle_evento', 'usuario')
    search_fields = ('activo__codigo', 'detalle_evento', 'usuario')
    list_filter = ('mmt_tipo', 'fecha_evento', 'usuario')


admin.site.register(HistorialGestion, HistorialGestionAdmin)