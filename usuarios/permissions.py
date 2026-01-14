# usuarios/permissions.py

from rest_framework import permissions

class IsAdminP(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.rol == 'AdminP'

class IsAdminC(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.rol == 'AdminC'

class IsProfesor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.rol == 'profesor'

class IsEstudiante(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.rol == 'estudiante'

class IsAdminCOrAdminP(permissions.BasePermission):
    """
    Permite solo a usuarios con rol 'AdminC' o 'AdminP'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol in ['AdminC', 'AdminP']
