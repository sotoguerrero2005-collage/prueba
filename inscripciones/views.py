# inscripciones/views.py
from rest_framework import viewsets, permissions
from .models import Inscripcion
from .serializers import InscripcionSerializer

class InscripcionViewSet(viewsets.ModelViewSet):
    serializer_class = InscripcionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Inscripcion.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        if user.rol == 'estudiante':
            # El estudiante solo ve sus inscripciones
            return Inscripcion.objects.filter(estudiante=user)
        return Inscripcion.objects.all()

    def perform_create(self, serializer):
        # Asignar automáticamente el estudiante que crea la inscripción
        serializer.save(estudiante=self.request.user, estado='pendiente')