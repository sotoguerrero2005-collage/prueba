# lecciones/serializers.py
from rest_framework import serializers
from .models import Leccion, RecursoLeccion
from cursos.models import Modulo

class RecursoLeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecursoLeccion
        fields = ['id', 'tipo', 'archivo', 'url_enlace', 'descripcion', 'orden']

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
        # 1. Extraer recursos para evitar error de relación inversa
        recursos_data = validated_data.pop('recursos', [])
        
        # 2. Crear la lección una sola vez
        leccion = Leccion.objects.create(**validated_data)

        # 3. Obtener el request del contexto
        request = self.context.get('request')
        
        if request:
            i = 0
            # Buscamos en request.data lo enviado desde el FormData de Angular
            while f'recursos[{i}]tipo' in request.data:
                tipo = request.data.get(f'recursos[{i}]tipo')
                descripcion = request.data.get(f'recursos[{i}]descripcion', '')
                orden = request.data.get(f'recursos[{i}]orden', i)
                url_enlace = request.data.get(f'recursos[{i}]url_enlace', '')
                archivo = request.FILES.get(f'recursos[{i}]archivo')

                RecursoLeccion.objects.create(
                    leccion=leccion,
                    tipo=tipo,
                    archivo=archivo,
                    url_enlace=url_enlace,
                    descripcion=descripcion,
                    orden=orden
                )
                i += 1
        
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
