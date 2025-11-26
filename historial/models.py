from django.db import models
from django.conf import settings
from activos.models import Activo

class HistorialGestion(models.Model):
    MMT_TIPO_CHOICES = [
        ('preventivo', 'Preventivo'),
        ('predictivo', 'Predictivo'),
        ('correctivo', 'Correctivo'),
        ('inspeccion', 'Inspección'),
    ]

    activo = models.ForeignKey(Activo, on_delete=models.CASCADE, related_name='activo_historial', verbose_name="Activo")
    fecha_evento = models.DateTimeField(auto_now_add=True)
    referencia_id = models.PositiveIntegerField() # Código del plan u OT
    mmt_tipo = models.CharField(max_length=20, choices=MMT_TIPO_CHOICES, db_index=True, verbose_name="Tipo de mantenimiento")
    detalle_evento = models.TextField(verbose_name="Detalle del evento")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='historial_user')

    class Meta:
        verbose_name = 'Historial de gestión'
        verbose_name_plural = 'Historiales de gestión'
        ordering = ['-fecha_evento']
        indexes = [
            models.Index(fields=['mmt_tipo', 'fecha_evento']),
            models.Index(fields=['activo', 'fecha_evento']),
        ]

    def __str__(self):
        return f'{self.activo.codigo} - {self.mmt_tipo} - {self.fecha_evento:%Y-%m-%d}'
