# inscripciones/serializers.py
from rest_framework import serializers
from .models import Inscripcion
from cursos.serializers import CursoSerializer
from cursos.models import Curso

class InscripcionSerializer(serializers.ModelSerializer):
    estudiante = serializers.ReadOnlyField(source='estudiante.username')

    # LECTURA: curso completo
    curso = CursoSerializer(read_only=True)

    # ESCRITURA: solo el ID
    curso_id = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(),
        source='curso',
        write_only=True
    )

    class Meta:
        model = Inscripcion
        fields = ['id', 'estudiante', 'curso', 'curso_id', 'estado', 'fecha_inscripcion']
        read_only_fields = [ 'id', 'estudiante', 'estado', 'fecha_inscripcion' ]

    def validate(self, data):
        usuario = self.context['request'].user
        curso = data.get('curso')

        print("DEBUG USER:", usuario, usuario.id_usuario)
        print("DEBUG CURSO:", curso, curso.id if curso else None)

        qs = Inscripcion.objects.filter(estudiante=usuario, curso=curso)
        print("DEBUG QUERYSET:", qs)

        if qs.exists():
            raise serializers.ValidationError(
                {"detail": "Ya estás inscrito en este curso"}
            )

        return data