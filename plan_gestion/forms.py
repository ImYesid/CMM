from django import forms
from django.utils.safestring import mark_safe
from .models import *

class PlanGestionForm(forms.ModelForm):
    class Meta:
        model = PlanGestion
        fields = ['plan_nombre', 'frecuencia', 'plan_tipo', 'descripcion']

    def __init__(self, *args, **kwargs):
        plan_tipo_fijo = kwargs.pop('plan_tipo_fijo', None)
        super().__init__(*args, **kwargs)

        if plan_tipo_fijo:
            self.fields['plan_tipo'].initial = plan_tipo_fijo
            self.fields['plan_tipo'].disabled = True
