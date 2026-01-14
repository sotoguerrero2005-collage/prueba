# inscripciones/serializers.py
from rest_framework import serializers
from .models import Inscripcion
from cursos.serializers import CursoSerializer
from cursos.models import Curso

class InscripcionSerializer(serializers.ModelSerializer):
    estudiante = serializers.ReadOnlyField(source='estudiante.username')

    # 🔹 LECTURA: curso completo
    curso = CursoSerializer(read_only=True)

    # 🔹 ESCRITURA: solo el ID
    curso_id = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(),
        source='curso',
        write_only=True
    )

    class Meta:
        model = Inscripcion
        fields = ['id', 'estudiante', 'curso', 'curso_id', 'estado', 'fecha_inscripcion', 'pago']

    def validate(self, data):
        usuario = self.context['request'].user
        curso = data['curso']
        if Inscripcion.objects.filter(estudiante=usuario, curso=curso).exists():
            raise serializers.ValidationError({
                "error": "El estudiante ya está inscrito en este curso."
            })
        return data
