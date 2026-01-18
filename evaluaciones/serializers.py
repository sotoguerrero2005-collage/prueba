# evaluaciones/serializers.py
from rest_framework import serializers
from .models import Evaluacion, Pregunta, Respuesta, IntentoEvaluacion, RespuestaAlumno

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = ['id', 'texto', 'es_correcta']

class PreguntaSerializer(serializers.ModelSerializer):
    respuestas = RespuestaSerializer(many=True)
    
    class Meta:
        model = Pregunta
        fields = ['id', 'texto', 'tipo', 'puntaje', 'respuestas']

class EvaluacionSerializer(serializers.ModelSerializer):
    preguntas = PreguntaSerializer(many=True)
    
    class Meta:
        model = Evaluacion
        fields = ['id', 'curso', 'titulo', 'descripcion', 'estado', 'preguntas']

    def create(self, validated_data):
        preguntas_data = validated_data.pop('preguntas')
        evaluacion = Evaluacion.objects.create(**validated_data)
        
        for pregunta_data in preguntas_data:
            respuestas_data = pregunta_data.pop('respuestas')
            pregunta = Pregunta.objects.create(evaluacion=evaluacion, **pregunta_data)
            
            for respuesta_data in respuestas_data:
                Respuesta.objects.create(pregunta=pregunta, **respuesta_data)
        return evaluacion  

class RespuestaAlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaAlumno
        fields = ['id', 'intento', 'pregunta', 'respuesta']

class IntentoEvaluacionSerializer(serializers.ModelSerializer):
    respuestas = RespuestaAlumnoSerializer(many=True, read_only=True)
    
    class Meta:
        model = IntentoEvaluacion
        fields = ['id', 'estudiante', 'evaluacion', 'fecha_inicio', 'fecha_fin', 'nota_total', 'estado', 'respuestas']