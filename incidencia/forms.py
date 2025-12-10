from django import forms
from django.utils.safestring import mark_safe
from .models import Incidencia

class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = [
            'activo',
            'nivel_prioridad',
            'OT',
            'estado',
            'descripcion'
        ]
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f"Ingrese {field.label if field.label else field_name.lower()}"
                })
        
            # Etiqueta en negrita con asterisco si es requerido
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color:red;'>*</span>")

        self.fields['nivel_prioridad'].empty_label = "Seleccione una prioridad"
        self.fields['nivel_prioridad'].widget.attrs.update({'class': 'form-select'})  
        self.fields['estado'].empty_label = "Seleccione un estado"
        self.fields['estado'].widget.attrs.update({'class': 'form-select'}) 