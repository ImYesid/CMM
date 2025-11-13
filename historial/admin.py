from django.contrib import admin
from .models import *

class HistorialGestionAdmin(admin.ModelAdmin):
    list_display = ('id_historia', 'activo', 'fecha_evento', 'mmt_tipo', 'detalle_evento', 'responsable',)
    search_fields = ('activo', 'fecha_evento', 'mmt_tipo', 'detalle_evento', 'responsable',)
    list_filter = ('fecha_evento','responsable',)


admin.site.register(HistorialGestion, HistorialGestionAdmin)