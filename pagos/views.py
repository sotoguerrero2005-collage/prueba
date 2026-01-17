from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import serializers
from django.utils import timezone
from .permissions import IsAdminPago, IsOwnerPago
from .serializers import PagoSerializer
from .models import Pago

class PagoViewSet(viewsets.ModelViewSet):
    serializer_class = PagoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Pago.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]

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

        pago_existente = Pago.objects.filter(inscripcion=inscripcion).first()

        if pago_existente:
            if pago_existente.estado in ['pendiente', 'aprobado']:
                raise serializers.ValidationError(
                    "Ya existe un pago pendiente o aprobado para esta inscripción."
                )
            elif pago_existente.estado == 'rechazado':
                pago_existente.metodo_pago = serializer.validated_data['metodo_pago']
                pago_existente.referencia = serializer.validated_data['referencia']
                pago_existente.monto = serializer.validated_data['monto']
                if 'captura_comprobante' in serializer.validated_data:
                    pago_existente.captura_comprobante = serializer.validated_data['captura_comprobante']
                pago_existente.estado = 'pendiente'
                pago_existente.motivo_rechazo = ''
                pago_existente.verificado_por = None
                pago_existente.fecha_verificacion = None
                pago_existente.save()
                serializer.instance = pago_existente
                return

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

        pago.inscripcion.estado = 'aprobado'
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

    def create(self, request, *args, **kwargs):
        try:
            inscripcion_id = int(request.data.getlist('inscripcion')[0])
            metodo_pago = request.data.getlist('metodo_pago')[0]
            referencia = request.data.getlist('referencia')[0]
            monto = float(request.data.getlist('monto')[0])
            captura_comprobante = request.FILES.get('captura_comprobante')

            data = {
                'inscripcion': inscripcion_id,
                'metodo_pago': metodo_pago,
                'referencia': referencia,
                'monto': monto,
                'captura_comprobante': captura_comprobante
            }

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except (ValueError, IndexError):
            return Response(
                {'error': 'Datos inválidos en la solicitud'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
