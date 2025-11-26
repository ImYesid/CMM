from django import forms
from django.utils.safestring import mark_safe
from .models import *

class PlanGestionForm(forms.ModelForm):
    class Meta:
        model = PlanGestion
        fields = ['activo', 'plan_nombre', 'frecuencia', 'estado', 'descripcion', 'plan_tipo']

    def __init__(self, *args, **kwargs):
        plan_tipo_fijo = kwargs.pop('plan_tipo_fijo', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f"Ingrese {field.label if field.label else field_name.lower()}"
                })

        # Etiqueta en negrita con asterisco si es requerido
            if field.required:
                field.label = mark_safe(f"<strong>{field.label} <span style='color:red;'>*</span></strong>")

        self.fields['estado'].widget.attrs.update({'class': 'form-select'})
        self.fields['estado'].initial = 'habilitado'

        # Preseleccionar valor fijo
        if plan_tipo_fijo:
            self.initial['plan_tipo'] = plan_tipo_fijo
            
        

