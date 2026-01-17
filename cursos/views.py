# cursos/views.py
from rest_framework import viewsets, permissions
from rest_framework import status
from .models import Curso
from .serializers import CursoSerializer, CursoDetalleSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from inscripciones.models import Inscripcion

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CursoDetalleSerializer  # detalle con modulos y lecciones
        return CursoSerializer


    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mis_cursos(self, request):
        cursos = Curso.objects.filter(
            inscripciones__estudiante=request.user,
            inscripciones__estado='activa'
        ).distinct()

        serializer = CursoDetalleSerializer(cursos, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mis_cursos_profesor(self, request):
        if request.user.rol != 'profesor':
            return Response([], status=403)

        cursos = Curso.objects.filter(profesor=request.user)

        serializer = CursoSerializer(cursos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='mis-cursos-alumno')
    def mis_cursos_alumno(self, request):
        alumno = request.user
        cursos = Curso.objects.filter(
            inscripciones__estudiante=alumno,
            inscripciones__estado='aprobado'
        )
        serializer = CursoDetalleSerializer(cursos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def disponibles(self, request):
        cursos = Curso.objects.filter(
            estado='activo'
        ).exclude(
            inscripciones__estudiante=request.user,
            inscripciones__estado__in=['pendiente', 'activa']
        )

        serializer = CursoSerializer(cursos, many=True)
        return Response(serializer.data)