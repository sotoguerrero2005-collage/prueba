from rest_framework import serializers
from .models import Pago
from inscripciones.models import Inscripcion

class PagoSerializer(serializers.ModelSerializer):
    inscripcion = serializers.PrimaryKeyRelatedField(
        queryset=Inscripcion.objects.all()
    )

    curso_nombre = serializers.CharField(
        source='inscripcion.curso.titulo', read_only=True
    )
    inscripcion_usuario_nombre = serializers.CharField(
        source='inscripcion.estudiante.nombre_completo', read_only=True
    )
    comprobante_url = serializers.SerializerMethodField()

    class Meta:
        model = Pago
        fields = [
            'id',
            'inscripcion',
            'metodo_pago',
            'referencia',
            'monto',
            'captura_comprobante',
            'estado',
            'verificado_por',
            'motivo_rechazo',
            'fecha_pago',
            'fecha_verificacion',
            'inscripcion_usuario_nombre',
            'curso_nombre',
            'comprobante_url'
        ]
        read_only_fields = [
            'id',
            'estado',
            'verificado_por',
            'fecha_verificacion',
            'curso_nombre',
            'inscripcion_usuario_nombre',
            'comprobante_url',
            'fecha_pago'
        ]

    def validate(self, data):
        inscripcion = data.get('inscripcion')

        if inscripcion.estado == 'activa':
            raise serializers.ValidationError(
                'Esta inscripción ya está activa'
            )

        if not self.instance:
            pago_existente = Pago.objects.filter(inscripcion=inscripcion).first()
            if pago_existente:
                if pago_existente.estado == 'pendiente':
                    raise serializers.ValidationError(
                        'Ya existe un pago pendiente para esta inscripción'
                    )
                elif pago_existente.estado == 'aprobado':
                    raise serializers.ValidationError(
                        'Esta inscripción ya tiene un pago aprobado'
                    )

        return data

    def get_comprobante_url(self, obj):
        if isinstance(obj, dict):
            return None
        request = self.context.get('request')
        if obj.captura_comprobante and request:
            return request.build_absolute_uri(obj.captura_comprobante.url)
        return None
