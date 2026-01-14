# pagos/permissions.py
from rest_framework.permissions import BasePermission

class IsAdminPago(BasePermission):
    """
    Permite acceso solo a usuarios administradores de pagos
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.rol in ['AdminP']
        )

class IsOwnerPago(BasePermission):
    """
    Permite acceso solo al estudiante dueño del pago
    """

    def has_object_permission(self, request, view, obj):
        return obj.estudiante == request.user
