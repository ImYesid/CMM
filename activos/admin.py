from django.contrib import admin
from .models import *

class ActivoAdmin(admin.ModelAdmin):
    list_display = ('id_activo', 'codigo', 'nombre', 'tipo', 'ubicacion', 'estado_operativo','fecha_registro',)
    search_fields = ('codigo', 'nombre', 'tipo', 'ubicacion', 'estado_operativo','fecha_registro',)
    list_filter = ('codigo','estado_operativo',)


admin.site.register(Activo, ActivoAdmin)