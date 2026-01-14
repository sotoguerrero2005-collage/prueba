# evaluaciones/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Evaluacion, IntentoEvaluacion, RespuestaAlumno
from .serializers import EvaluacionSerializer, IntentoEvaluacionSerializer, RespuestaAlumnoSerializer

# CRUD de evaluaciones
class EvaluacionViewSet(viewsets.ModelViewSet):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer

# Intentos de evaluación
class IntentoEvaluacionViewSet(viewsets.ModelViewSet):
    queryset = IntentoEvaluacion.objects.all()
    serializer_class = IntentoEvaluacionSerializer

    # Filtrar intentos por estudiante logueado
    def get_queryset(self):
        user = self.request.user
        if user.rol == 'estudiante':
            return IntentoEvaluacion.objects.filter(estudiante=user)
        return IntentoEvaluacion.objects.all()

    # Endpoint para finalizar un intento
    @action(detail=True, methods=['post'])
    def finalizar(self, request, pk=None):
        """
        Finaliza un intento:
        - Calcula la nota total
        - Cambia estado a 'finalizado'
        - Registra fecha_fin
        """
        intento = self.get_object()
        if intento.estado != 'en_progreso':
            return Response(
                {'detail': 'Intento ya finalizado'},
                status=status.HTTP_400_BAD_REQUEST
            )

        intento.calcular_nota()
        serializer = self.get_serializer(intento)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Respuestas de alumno
class RespuestaAlumnoViewSet(viewsets.ModelViewSet):
    queryset = RespuestaAlumno.objects.all()
    serializer_class = RespuestaAlumnoSerializer
