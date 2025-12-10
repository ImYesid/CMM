from django import forms
from django.utils.safestring import mark_safe
from .models import Usuario, User_feedback

class CustomPasswordInput(forms.PasswordInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        icon_html = """<a href="javascript:;" class="input-group-text bg-transparent" id="togglePassword">
                        <i class='bx bx-hide'></i>
                        </a>"""
        return mark_safe(f"<div class='input-group'>{html}{icon_html}</div>")

class LoginForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'email']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        # Form login 
        self.fields['username'] = forms.CharField(
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresar Usuario',
                'id': 'inputDocumento',
                'required': 'required'
            })   
        )
        self.fields['password'] = forms.CharField(
            widget=CustomPasswordInput(attrs={
            'placeholder': "Ingresar Contraseña",
            'id': "inputChoosePassword",
            'class': "form-control border-end-0",
            'required': 'required'
            })
        )

        # form password recovery
        self.fields['email']= forms.CharField(widget=forms.EmailInput(attrs={
            'placeholder': "Tu correo electrónico",
            'class': "form-control-lg"
        }))


        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class User_feedbackForm(forms.ModelForm):
    class Meta:
        model = User_feedback
        fields = ['calificacion','comentario']
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

        self.fields['calificacion'].empty_label = "Seleccione una Calificación"
        self.fields['calificacion'].widget.attrs.update({'class': 'form-select'})   