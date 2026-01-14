from django.db import models
from usuarios.models import Usuario

class Pago(models.Model):
    METODO_CHOICES = [
        ('transferencia', 'Transferencia'),
        ('pago_movil', 'Pago Móvil')
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado')
    ]
    
    inscripcion = models.OneToOneField('inscripciones.Inscripcion', on_delete=models.CASCADE, related_name='pago')
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pagos')
    metodo_pago = models.CharField(max_length=30, choices=METODO_CHOICES)
    referencia = models.CharField(max_length=100, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    captura_comprobante = models.ImageField(upload_to='comprobantes/', null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    verificado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL,
                                       null=True, blank=True,
                                       related_name='pagos_verificados')
    motivo_rechazo = models.TextField(blank=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    fecha_verificacion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.inscripcion} - {self.estado}"
