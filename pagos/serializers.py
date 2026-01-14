# pagos/serializers.py
from rest_framework import serializers
from .models import Pago

class PagoSerializer(serializers.ModelSerializer):

    curso_nombre = serializers.CharField(
        source='inscripcion.curso.nombre',
        read_only=True
    )
    inscripcion_usuario_nombre = serializers.CharField(source='inscripcion.estudiante.nombre_completo')  # <--- esto

    comprobante_url = serializers.SerializerMethodField()

    class Meta:
        model = Pago
        fields = [
            'id',
            'inscripcion',
            'estudiante',
            'metodo_pago',
            'referencia',
            'monto',
            'captura_comprobante',
            'estado',
            'verificado_por',
            'motivo_rechazo',
            'fecha_pago',
            'fecha_verificacion'
        ]

    def get_comprobante_url(self, obj):
        request = self.context.get('request')
        if obj.captura_comprobante and request:
            return request.build_absolute_uri(obj.captura_comprobante.url)
        return None

    read_only_fields = [
        'estado',
        'verificado_por',
        'fecha_verificacion'
    ]