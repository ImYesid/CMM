from django.db import models

class Activo(models.Model):
    ESTADOS_OPERATIVOS_CHOICES = [
        ('operativo', 'Operativo'),
        ('inoperativo', 'Inoperativo'),
        ('mantenimiento', 'En mantenimiento'),
        ('retirado', 'Retirado'),
    ]

    id_activo = models.BigAutoField(primary_key=True)
    codigo = models.CharField(max_length=50, unique=True, db_index=True)
    nombre = models.CharField(max_length=120)
    tipo = models.CharField(max_length=60, db_index=True)
    ubicacion = models.CharField(max_length=120, db_index=True)
    estado_operativo = models.CharField(max_length=20, choices=ESTADOS_OPERATIVOS_CHOICES, default='operativo', db_index=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Activo'
        verbose_name_plural = 'Activos'
        indexes = [
            models.Index(fields=['tipo']),
            models.Index(fields=['ubicacion']),
            models.Index(fields=['estado_operativo']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['codigo'], name='uq_activo_codigo'),
        ]

    def __str__(self):
        return f'{self.code} - {self.name}'
