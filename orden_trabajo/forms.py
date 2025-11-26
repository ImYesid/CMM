from django import forms
from django.utils.safestring import mark_safe
from .models import OrdenTrabajo

class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = [
            'activo', 'plan', 'descripcion_falla', 'acciones',
            'fecha_inicio', 'fecha_fin', 'OT_estado', 'recursos_usados',
            'tiempo_intervencion', 'usuario'
        ]
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'tiempo_intervencion': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f"Ingrese {field.label if field.label else field_name.lower()}"
                })
        
            # Etiqueta en negrita con asterisco si es requerido
            if field.required:
                field.label = mark_safe(f"<strong>{field.label} <span style='color:red;'>*</span></strong>")

        self.fields['OT_estado'].empty_label = "Seleccione un estado"
        self.fields['OT_estado'].widget.attrs.update({'class': 'form-select'})