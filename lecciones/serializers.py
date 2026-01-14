# lecciones/serializers.py
from rest_framework import serializers
from .models import Leccion, RecursoLeccion
from cursos.models import Modulo

class RecursoLeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecursoLeccion
        fields = ['id', 'tipo', 'url_archivo', 'descripcion', 'orden']

class LeccionSerializer(serializers.ModelSerializer):
    recursos = RecursoLeccionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Leccion
        fields = ['id', 'modulo', 'titulo', 'contenido', 'orden', 'recursos']

class LeccionCreateSerializer(serializers.ModelSerializer):
    recursos = RecursoLeccionSerializer(many=True, required=False)

    class Meta:
        model = Leccion
        fields = ['id', 'modulo', 'titulo', 'contenido', 'orden', 'recursos']

    def create(self, validated_data):
        recursos_data = validated_data.pop('recursos', [])
        leccion = Leccion.objects.create(**validated_data)
        for recurso_data in recursos_data:
            RecursoLeccion.objects.create(leccion=leccion, **recurso_data)
        return leccion

class LeccionPreviewSerializer(serializers.ModelSerializer):
    contenido = serializers.SerializerMethodField()

    class Meta:
        model = Leccion
        fields = ['id', 'titulo', 'contenido', 'orden']

    def get_contenido(self, obj):
        inscrito = self.context.get('inscrito', False)
        if inscrito:
            return obj.contenido
        return None  # preview

class ModuloDetalleSerializer(serializers.ModelSerializer):
    lecciones = LeccionPreviewSerializer(many=True)

    class Meta:
        model = Modulo
        fields = ['id', 'titulo', 'orden', 'lecciones']
