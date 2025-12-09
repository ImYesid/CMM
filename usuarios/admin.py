from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, PerfilUsuario, Cargo, User_feedback

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'last_login',)
    search_fields = ('username', 'email',)
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        ("Información del Usuario", {'fields': ('username', 'email', 'password')}),
        ("Permisos", {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ("Fechas", {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active',)
        }),
    )

class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre', 'apellido', 'documento', 'telefono', 'cargo',)
    search_fields = ('nombre', 'apellido', 'documento', 'telefono', 'cargo',)
    list_filter = ('usuario__is_active',)

class CargoAdmin(admin.ModelAdmin):
    list_display = ('cargo',)
    search_fields = ('cargo',)

class User_feedbackAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'orden_trabajo', 'calificacion', 'comentario', 'fecha_registro',)
    search_fields = ('usuario', 'calificacion',)

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(User_feedback, User_feedbackAdmin)
