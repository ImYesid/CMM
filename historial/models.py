from django.db import models
from activos.models import Activo

class HistorialGestion(models.Model):
    MMT_TIPO_CHOICES = [
        ('preventivo', 'Preventivo'),
        ('predictivo', 'Predictivo'),
        ('correctivo', 'Correctivo'),
        ('inspeccion', 'Inspección'),
    ]

    activo = models.ForeignKey(Activo, on_delete=models.CASCADE, related_name='activo_historial')
    fecha_evento = models.DateTimeField()
    mmt_tipo = models.CharField(max_length=20, choices=MMT_TIPO_CHOICES, db_index=True)
    detalle_evento = models.TextField()
    responsable = models.CharField(max_length=120)

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
