# cursos/serializers.py
from rest_framework import serializers
from .models import Curso, Modulo
from lecciones.serializers import ModuloDetalleSerializer
from evaluaciones.serializers import EvaluacionSerializer


class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = ['id', 'titulo', 'orden', 'curso']
        read_only_fields = ['id', 'curso']


class CursoSerializer(serializers.ModelSerializer):
    modulos = ModuloSerializer(many=True, required=False)

    class Meta:
        model = Curso
        fields = [
            'id',
            'titulo',
            'descripcion_breve',
            'descripcion',
            'imagen',
            'precio',
            'estado',
            'fecha_creacion',
            'profesor',
            'modulos',
        ]

    def validate_profesor(self, value):
        if value.rol != 'profesor':
            raise serializers.ValidationError(
                "El usuario seleccionado no tiene rol de profesor"
            )
        return value

    def create(self, validated_data):
        modulos_data = validated_data.pop('modulos', [])
        curso = Curso.objects.create(**validated_data)

        for modulo_data in modulos_data:
            Modulo.objects.create(curso=curso, **modulo_data)

        return curso

    def update(self, instance, validated_data):
        modulos_data = validated_data.pop('modulos', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        instance.modulos.all().delete()
        for modulo_data in modulos_data:
            Modulo.objects.create(curso=instance, **modulo_data)

        return instance


class CursoDetalleSerializer(serializers.ModelSerializer):
    modulos = ModuloDetalleSerializer(many=True)
    evaluaciones = EvaluacionSerializer(many=True)
    inscrito = serializers.SerializerMethodField()
    estadoInscripcion = serializers.SerializerMethodField()

    class Meta:
        model = Curso
        fields = [
            'id',
            'titulo',
            'descripcion_breve',
            'descripcion',
            'imagen',
            'precio',
            'estado',
            'fecha_creacion',
            'profesor',
            'modulos',
            'evaluaciones',
            'inscrito',
            'estadoInscripcion'
        ]

    def get_inscrito(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.inscripciones.filter(
            estudiante=request.user,
            estado='aprobado'
        ).exists()

    def get_estadoInscripcion(self, obj):
        """Retorna 'pendiente', 'aprobado' o 'rechazado' para este usuario"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None
        inscripcion = obj.inscripciones.filter(estudiante=request.user).first()
        return inscripcion.estado if inscripcion else None        

    def to_representation(self, instance):
        data = super().to_representation(instance)
        inscrito = data['inscrito']

        for modulo in data['modulos']:
            for leccion in modulo['lecciones']:
                if not inscrito:
                    leccion['contenido'] = None

        return data
