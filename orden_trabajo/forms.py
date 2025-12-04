from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from .models import OrdenTrabajo

class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = [
            'activo', 'tecnico_asignado', 'plan', 'fecha_inicio',
            'fecha_fin', 'tiempo_intervencion', 'OT_estado', 'descripcion_falla',
            'acciones', 'recursos_usados'
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'fecha_fin': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'tiempo_intervencion': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get("OT_estado")
        acciones = cleaned_data.get("acciones")
        recursos = cleaned_data.get("recursos_usados")

        if estado == "cerrada":
            if not acciones or not recursos:
                raise ValidationError("Debe diligenciar acciones y recursos usados antes de cerrar la OT.")

        return cleaned_data

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

        self.fields['OT_estado'].empty_label = "Seleccione un estado"
        self.fields['OT_estado'].widget.attrs.update({'class': 'form-select'})