from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("El usuario debe tener una dirección de correo electrónico.")

        if not username:
            raise ValueError("El usuario debe tener un nombre de usuario")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):   
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class Usuario(AbstractBaseUser, PermissionsMixin):
    username                = models.CharField(max_length=50, unique=True)
    email                   = models.EmailField(max_length=100, unique=True)

    # required
    date_joined             = models.DateTimeField(auto_now_add=True)
    last_login              = models.DateTimeField(auto_now_add=True)
    is_staff                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    #is_superadmin           = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return self.username
    
class Cargo(models.Model):
    CARGO_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Supervisor', 'Supervisor'),
        ('Tecnico', 'Tecnico'),
    ]
    cargo  = models.CharField(max_length=50, choices=CARGO_CHOICES, default='Tecnico')

    def __str__(self):
        return self.cargo

class PerfilUsuario(models.Model):
    usuario     = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre      = models.CharField(max_length=50)
    apellido    = models.CharField(max_length=50)
    documento   = models.IntegerField(unique=True)
    telefono    = models.IntegerField(unique=True)
    cargo       = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name="Cargo")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def full_name(self):
        return f'{self.nombre} {self.apellido}'
    


class ConfiguracionUsuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    # Opciones de personalización
    tema = models.CharField(max_length=20, choices=[
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('semidark', 'Semi Dark'),
        ('minimal', 'Minimal'),
    ], default='semidark')

    color_encabezado = models.CharField(max_length=20, default='headercolor1')
    color_sidebar = models.CharField(max_length=20, default='sidebarcolor1')

    def __str__(self):
        return f"Configuración de {self.usuario.username}"