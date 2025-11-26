from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from activos.models import Activo
from plan_gestion.models import PlanGestion

class OrdenTrabajo(models.Model):
    OT_ESTADO_CHOICES = [
        ('abierta', 'Abierta'),
        ('en_ejecucion', 'En ejecución'),
        ('cerrada', 'Cerrada'),
        ('bloqueada', 'Bloqueada'),
    ]
    codigo = models.CharField(max_length=50, unique=True)
    activo = models.ForeignKey(Activo, on_delete=models.PROTECT, related_name='activo_ordenes')
    plan = models.ForeignKey(PlanGestion, on_delete=models.SET_NULL, null=True, blank=True, related_name='plan_ordenes')
    descripcion_falla = models.TextField()
    acciones = models.TextField(blank=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    OT_estado = models.CharField(max_length=15, choices=OT_ESTADO_CHOICES, default='abierta', db_index=True)
    recursos_usados = models.TextField(blank=True)  # materiales/herramientas/horas
    tiempo_intervencion = models.DurationField(null=True, blank=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_asignadas')

    def save(self, *args, **kwargs):
        if not self.pk:  # Si la instancia es nueva (sin PK)
            # Generar número consecutivo
            if not self.codigo:
                año = timezone.now().year
                with transaction.atomic():
                    ultima_OT = OrdenTrabajo.objects.filter(
                        codigo__startswith=f"OT-{año}-"
                    ).order_by('-codigo').first()

                    if ultima_OT:
                        ultimo_numero = int(ultima_OT.codigo.split("-")[-1])
                    else:
                        ultimo_numero = 0

                    nuevo_numero = ultimo_numero + 1
                    self.codigo = f"OT-{año}-{nuevo_numero:04d}"

            super().save(*args, **kwargs) # Guarda la instancia por primera vez
            
    class Meta:
        verbose_name = 'Orden de trabajo'
        verbose_name_plural = 'Órdenes de trabajo'
        ordering = ['-fecha_inicio']
        indexes = [
            models.Index(fields=['OT_estado']),
            models.Index(fields=['activo', 'OT_estado']),
            models.Index(fields=['plan']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(fecha_fin__gte=models.F('fecha_inicio')) | models.Q(fecha_fin__isnull=True), name='ck_wo_end_after_start'
            ),
        ]

    def __str__(self):
        return f'{self.codigo}/({self.activo.codigo})'
