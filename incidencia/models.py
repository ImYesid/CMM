from django.conf import settings
from django.db import models
from activos.models import Activo
from orden_trabajo.models import OrdenTrabajo

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
    activo = models.ForeignKey(Activo, on_delete=models.PROTECT, related_name='activo_incidencias')
    descripcion = models.TextField()
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    nivel_prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, db_index=True)
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='reportada', db_index=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='incidencias_reportadas')
    OT = models.ForeignKey(OrdenTrabajo, on_delete=models.PROTECT,  related_name='OT_incidencia')

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
        return f'Inc- {self.activo.codigo} [{self.nivel_prioridad}]'
