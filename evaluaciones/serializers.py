# evaluaciones/serializers.py
from rest_framework import serializers
from .models import Evaluacion, Pregunta, Respuesta, IntentoEvaluacion, RespuestaAlumno

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = ['id', 'pregunta', 'texto', 'es_correcta']

class PreguntaSerializer(serializers.ModelSerializer):
    respuestas = RespuestaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pregunta
        fields = ['id', 'evaluacion', 'texto', 'tipo', 'puntaje', 'respuestas']

class EvaluacionSerializer(serializers.ModelSerializer):
    preguntas = PreguntaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Evaluacion
        fields = ['id', 'curso', 'titulo', 'estado', 'preguntas']

class RespuestaAlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaAlumno
        fields = ['id', 'intento', 'pregunta', 'respuesta']

class IntentoEvaluacionSerializer(serializers.ModelSerializer):
    respuestas = RespuestaAlumnoSerializer(many=True, read_only=True)
    
    class Meta:
        model = IntentoEvaluacion
        fields = ['id', 'estudiante', 'evaluacion', 'fecha_inicio', 'fecha_fin', 'nota_total', 'estado', 'respuestas']