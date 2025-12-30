from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Curso, Inscripcion, ContenidoCurso, Evaluacion
from .serializers import CursoSerializer, InscripcionSerializer, ContenidoCursoSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def disponibles(self, request):
        cursos = Curso.objects.filter(estado='activo')
        serializer = self.get_serializer(cursos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mis_cursos(self, request):
        
        # Es mejor verificar si el usuario es estudiante
        inscripciones = Inscripcion.objects.filter(alumno=request.user)
        cursos = [i.curso for i in inscripciones.select_related('curso')]
        serializer = self.get_serializer(cursos, many=True)
        return Response(serializer.data)

    # NUEVO: Endpoint para ver el contenido de un curso específico
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def contenido(self, request, pk=None):
        """URL: /api/cursos/{id}/contenido/"""
        curso = self.get_object()
        contenidos = ContenidoCurso.objects.filter(curso=curso)
        serializer = ContenidoCursoSerializer(contenidos, many=True)
        return Response(serializer.data)