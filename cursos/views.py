# cursos/views.py
from rest_framework import viewsets, permissions
from .models import Curso
from .serializers import CursoSerializer, CursoDetalleSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CursoDetalleSerializer  # 🔹 detalle con modulos y lecciones
        return CursoSerializer
