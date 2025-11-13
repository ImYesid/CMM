from django.db import models

class PlanGestion(models.Model):
    PLAN_TIPO_CHOICES = [
        ('preventivo', 'Preventivo'),
        ('predictivo', 'Predictivo'),
        ('correctivo', 'Correctivo'),
        ('inspeccion', 'Inspección'),
    ]
    FRECUENCIA_CHOICES = [
        ('diaria', 'Diaria'),
        ('semanal', 'Semanal'),
        ('mensual', 'Mensual'),
        ('trimestral', 'Trimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
        ('ciclos', 'Por ciclos/uso'),
    ]

    id_plan = models.BigAutoField(primary_key=True)
    plan_nombre = models.CharField(max_length=120, unique=True, db_index=True)
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIA_CHOICES, db_index=True)
    plan_tipo = models.CharField(max_length=20, choices=PLAN_TIPO_CHOICES, db_index=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Plan de gestión'
        verbose_name_plural = 'Planes de gestión'
        indexes = [
            models.Index(fields=['plan_tipo']),
            models.Index(fields=['frecuencia']),
        ]

    def __str__(self):
        return f'{self.plan_nombre} ({self.plan_tipo}/{self.frecuencia})'
