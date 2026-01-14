from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, UserActivity

@receiver(post_save, sender=Usuario)
def registrar_actividad_usuario(sender, instance, created, **kwargs):
    """
    Registra automáticamente las actividades importantes de un usuario:
    - Creación
    - Actualización general (sin incluir activación/desactivación explícita)
    """
    if created:
        action = f"Usuario creado: {instance.correo}"
        UserActivity.objects.create(user=instance, action=action)
    else:
        # Evitamos registrar actualización si el cambio fue solo activar/desactivar
        # Para esto, suponemos que activación/desactivación se hace con métodos del ViewSet
        if not hasattr(instance, '_skip_update_log'):
            action = f"Usuario actualizado: {instance.correo}"
            UserActivity.objects.create(user=instance, action=action)


# Funciones helper para activar/desactivar usuarios y registrar actividad clara
def registrar_actividad_manual(usuario, accion, quien):
    """
    Registrar actividad manualmente desde el ViewSet u otros métodos.
    - usuario: objeto Usuario afectado
    - accion: string de la acción (ej: "Activó al usuario")
    - quien: Usuario que realizó la acción
    """
    UserActivity.objects.create(user=quien, action=f"{accion}: {usuario.correo}")
