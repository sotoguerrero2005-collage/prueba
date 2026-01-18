# lecciones/views.py
from rest_framework import viewsets, permissions
from .models import Leccion, RecursoLeccion
from .serializers import LeccionSerializer, RecursoLeccionSerializer, LeccionCreateSerializer
from inscripciones.models import Inscripcion
from rest_framework.parsers import MultiPartParser, FormParser

class LeccionViewSet(viewsets.ModelViewSet):
    queryset = Leccion.objects.all()
    serializer_class = LeccionSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return LeccionCreateSerializer
        return LeccionSerializer

    def get_queryset(self):
        # Solo mostrar lecciones de cursos donde el usuario está inscrito
        user = self.request.user
        if user.rol == 'estudiante':
            cursos = Inscripcion.objects.filter(estudiante=user, estado='activa').values_list('curso', flat=True)
            return Leccion.objects.filter(modulo__curso__in=cursos)
        elif user.rol == 'profesor':
            return Leccion.objects.filter(modulo__curso__profesor=user)
        return Leccion.objects.all()

    # Para que el serializer pueda leer request.data y request.FILES
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context        
