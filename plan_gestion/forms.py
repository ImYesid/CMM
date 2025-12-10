from django import forms
from django.utils.safestring import mark_safe
from .models import *

class PlanGestionForm(forms.ModelForm):
    class Meta:
        model = PlanGestion
        fields = ['plan_tipo', 
                  'activo', 
                  'plan_nombre', 
                  'estado', 
                  'descripcion', 
                  'frecuencia']

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
                field.label = mark_safe(f"{field.label} <span style='color:red;'>*</span>")

        self.fields['estado'].widget.attrs.update({'class': 'form-select'})
        self.fields['estado'].initial = 'habilitado'

        # Preseleccionar valor fijo
        if plan_tipo_fijo:
            self.initial['plan_tipo'] = plan_tipo_fijo
            self.fields['plan_tipo'].disabled = True
            
            
        

