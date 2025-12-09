from django import forms
from django.utils.safestring import mark_safe
from .models import Activo

class ActivoForm(forms.ModelForm):
    class Meta:
        model = Activo
        fields = ['nombre','tipo','estado_operativo','ubicacion']
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

        self.fields['estado_operativo'].empty_label = "Seleccione un estado operativo"
        self.fields['estado_operativo'].widget.attrs.update({'class': 'form-select'})   