# cursos/serializers.py
from rest_framework import serializers
from .models import Curso, Modulo
from lecciones.models import Leccion
from lecciones.serializers import ModuloDetalleSerializer

class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = ['id', 'titulo', 'orden', 'curso']
        read_only_fields = ['id', 'curso']

class CursoSerializer(serializers.ModelSerializer):
    modulos = ModuloSerializer(many=True)

    class Meta:
        model = Curso
        fields = ['id', 'titulo', 'descripcion_breve', 'descripcion', 'imagen', 'precio', 'estado', 'fecha_creacion', 'profesor', 'modulos']

    def create(self, validated_data):
        modulos_data = validated_data.pop('modulos', [])
        curso = Curso.objects.create(**validated_data)
        for modulo_data in modulos_data:
            Modulo.objects.create(curso=curso, **modulo_data)
        return curso

    def update(self, instance, validated_data):
        modulos_data = validated_data.pop('modulos', [])
        # Actualizar campos de curso
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Actualizar módulos: borrarlos y recrearlos (simple)
        instance.modulos.all().delete()
        for modulo_data in modulos_data:
            Modulo.objects.create(curso=instance, **modulo_data)
        return instance

class CursoDetalleSerializer(serializers.ModelSerializer):
    modulos = ModuloDetalleSerializer(many=True)
    inscrito = serializers.SerializerMethodField()

    class Meta:
        model = Curso
        fields = ['id', 'titulo', 'descripcion_breve', 'descripcion', 
                  'imagen', 'precio', 'estado', 'fecha_creacion', 'profesor', 
                  'modulos', 'inscrito']

    def get_inscrito(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.inscripciones.filter(estudiante=request.user, estado='activa').exists()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # marcar si está inscrito
        inscrito = data['inscrito']

        for modulo in data['modulos']:
            for leccion in modulo['lecciones']:
                if not inscrito:
                    leccion['contenido'] = None
                else:
                    # si quieres, aquí podrías pasar contenido completo
                    pass

        return data

