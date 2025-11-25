from django import forms
from django.utils.safestring import mark_safe
from .models import Activo

class ActivoForm(forms.ModelForm):
    class Meta:
        model = Activo
        fields = ['codigo','nombre','tipo','ubicacion','estado_operativo']
        widgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
            # Etiqueta en negrita con asterisco si es requerido
            if field.required:
                field.label = mark_safe(f"<strong>{field.label} <span style='color:red;'>*</span></strong>")

        self.fields['estado_operativo'].empty_label = "Seleccione un estado operativo"
        self.fields['estado_operativo'].widget.attrs.update({'class': 'form-select'})   