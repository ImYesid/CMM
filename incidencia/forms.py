from django import forms
from django.utils.safestring import mark_safe
from .models import Incidencia

class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = [
            'activo',
            'descripcion',
            'nivel_prioridad',
            'estado',
            'usuario',
            'OT'
        ]
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            # Etiqueta en negrita con asterisco si es requerido
            if field.required:
                field.label = mark_safe(f"<strong>{field.label} <span style='color:red;'>*</span></strong>")

        self.fields['nivel_prioridad'].empty_label = "Seleccione una prioridad"
        self.fields['nivel_prioridad'].widget.attrs.update({'class': 'form-select'})  
        self.fields['estado'].empty_label = "Seleccione un estado"
        self.fields['estado'].widget.attrs.update({'class': 'form-select'}) 