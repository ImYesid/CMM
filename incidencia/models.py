from django.conf import settings
from django.db import models
from activos.models import Activo

class Incidencia(models.Model):
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]
    ESTADO_CHOICES = [
        ('reportada', 'Reportada'),
        ('en_proceso', 'En proceso'),
        ('resuelta', 'Resuelta'),
        ('cancelada', 'Cancelada'),
    ]

    id_incidencia = models.BigAutoField(primary_key=True)
    activo = models.ForeignKey(Activo, on_delete=models.PROTECT, related_name='incidencias')
    descripcion = models.TextField()
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    nivel_prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, db_index=True)
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='reportada', db_index=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='incidencias_reportadas')

    class Meta:
        verbose_name = 'Incidencia'
        verbose_name_plural = 'Incidencias'
        ordering = ['-fecha_reporte']
        indexes = [
            models.Index(fields=['nivel_prioridad']),
            models.Index(fields=['estado']),
            models.Index(fields=['activo', 'estado']),
        ]

    def __str__(self):
        return f'Inc-{self.id_incidencia} {self.activo.codigo} [{self.nivel_prioridad}]'
