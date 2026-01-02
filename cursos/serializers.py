from rest_framework import serializers
from .models import Curso, ContenidoCurso, Inscripcion


class ContenidoCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContenidoCurso
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    # Esto permite que el curso incluya el nombre del profesor y sus contenidos
    nombre_profesor = serializers.ReadOnlyField(source='profesor.nombre_completo')
    contenidos = ContenidoCursoSerializer(many=True, read_only=True, source='contenidocurso_set')

    class Meta:
        model = Curso
        fields = [
            'id_curso', 'titulo', 'descripcion_breve', 'descripcion', 
            'imagen', 'precio', 'estado', 'nombre_profesor', 'contenidos'
        ]

class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = '__all__'
