from django.db import models, transaction
from django.utils import timezone

class Activo(models.Model):
    ESTADOS_OPERATIVOS_CHOICES = [
        ('operativo', 'Operativo'),
        ('inoperativo', 'Inoperativo'),
        ('mantenimiento', 'En mantenimiento'),
        ('retirado', 'Retirado'),
    ]
    TIPOS_CHOICES = [
        ('M/CNCC', 'Maquinaria de Mecanizado CNC y Convencional'),
        ('M/CE', 'Maquinaria de Conformado y Estampado'),
        ('E/SCT', 'Equipo de Soldadura y Corte Térmico'),
        ('E/ASS', 'Equipos Auxiliares y Sistemas de Soporte'),
        ('E/IMC', 'Equipos de Izaje y Movimiento de Carga'),
        ('E/MP', 'Herramientas y Equipos de Medición/Prueba'),
        ('I/ES', 'Instalaciones Eléctricas y Servicios'),
    ]
    codigo = models.CharField(max_length=50, unique=True, db_index=True)
    nombre = models.CharField(max_length=120)
    tipo = models.CharField(max_length=20, choices=TIPOS_CHOICES, db_index=True)
    ubicacion = models.CharField(max_length=120, db_index=True)
    estado_operativo = models.CharField(max_length=20, choices=ESTADOS_OPERATIVOS_CHOICES, default='operativo', db_index=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Si la instancia es nueva (sin PK)
            # Generar número consecutivo
            if not self.codigo:
                tipo = tipo
                año = timezone.now().year
                with transaction.atomic():
                    ultimo_Activo = Activo.objects.filter(
                        codigo__startswith=f"{tipo}-{año}-"
                    ).order_by('-codigo').first()

                    if ultimo_Activo:
                        ultimo_numero = int(ultimo_Activo.codigo.split("-")[-1])
                    else:
                        ultimo_numero = 0

                    nuevo_numero = ultimo_numero + 1
                    self.codigo = f"{tipo}-{año}-{nuevo_numero:03d}"

        super().save(*args, **kwargs)

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
        return f'{self.codigo} - {self.nombre}'
