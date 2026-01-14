# apps/inscripciones/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Inscripcion

@receiver(post_save, sender=Inscripcion)
def actualizar_estado_pago(sender, instance, **kwargs):
    if instance.pago and instance.pago.estado == 'aprobado':
        instance.estado = 'activa'
        instance.save()
