from django.contrib import admin
from .models import *

class PlanGestionAdmin(admin.ModelAdmin):
    list_display = ('id_plan', 'plan_nombre', 'frecuencia', 'plan_tipo', 'descripcion',)
    search_fields = ('plan_nombre', 'frecuencia', 'plan_tipo', 'descripcion',)
    list_filter = ('plan_nombre','plan_tipo',)


admin.site.register(PlanGestion, PlanGestionAdmin)