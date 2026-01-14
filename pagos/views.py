# pagos/views.py
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from django.utils import timezone
from .permissions import IsAdminPago, IsOwnerPago
from .serializers import PagoSerializer
from .models import Pago

class PagoViewSet(viewsets.ModelViewSet):
    serializer_class = PagoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Pago.objects.all() 

    def get_queryset(self):
        user = self.request.user

        if user.rol in ['AdminP', 'AdminC']:
            return Pago.objects.all()

        return Pago.objects.filter(estudiante=user)

    def get_permissions(self):
        if self.action in ['aprobar', 'rechazar', 'pendientes']:
            permission_classes = [IsAdminPago]
        elif self.action in ['retrieve']:
            permission_classes = [IsOwnerPago]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        inscripcion = serializer.validated_data['inscripcion']

        if inscripcion.estado == 'activa':
            raise ValidationError('Esta inscripción ya está activa')

        serializer.save(estudiante=self.request.user)

    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        pagos = Pago.objects.filter(estado='pendiente')
        serializer = self.get_serializer(pagos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminPago])
    def aprobar(self, request, pk=None):
        pago = self.get_object()

        if pago.estado != 'pendiente':
            return Response(
                {'error': 'Este pago ya fue procesado'},
                status=400
            )

        pago.estado = 'aprobado'
        pago.verificado_por = request.user
        pago.fecha_verificacion = timezone.now()

        pago.inscripcion.estado = 'activa'
        pago.inscripcion.save()

        pago.save()

        return Response({'status': 'pago aprobado'})

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminPago])
    def rechazar(self, request, pk=None):
        pago = self.get_object()

        motivo = request.data.get('motivo')
        if not motivo:
            return Response(
                {'error': 'Debe indicar el motivo del rechazo'},
                status=400
            )

        pago.estado = 'rechazado'
        pago.motivo_rechazo = motivo
        pago.verificado_por = request.user
        pago.fecha_verificacion = timezone.now()
        pago.save()

        return Response({'status': 'pago rechazado'})