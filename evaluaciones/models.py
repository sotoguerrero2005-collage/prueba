from django.db import models
from cursos.models import Curso
from usuarios.models import Usuario
from django.utils import timezone

class Evaluacion(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva')
    ]
    
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='evaluaciones')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"

class Pregunta(models.Model):
    TIPO_CHOICES = [
        ('seleccion', 'Selección múltiple'),
        ('verdadero_falso', 'Verdadero/Falso')
    ]
    
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='preguntas')
    texto = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='seleccion')
    puntaje = models.DecimalField(max_digits=5, decimal_places=2, default=1)

    def __str__(self):
        return f"{self.evaluacion.titulo} - Pregunta"

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='respuestas')
    texto = models.TextField()
    es_correcta = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.pregunta.id} - {self.texto[:30]}"

class IntentoEvaluacion(models.Model):
    estudiante = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'estudiante'},
        related_name='intentos'
    )
    evaluacion = models.ForeignKey(
        Evaluacion,
        on_delete=models.CASCADE,
        related_name='intentos'
    )
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    nota_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('en_progreso', 'En progreso'),
            ('finalizado', 'Finalizado'),
            ('corregido', 'Corregido')
        ]
    )

    def calcular_nota(self):
        """
        Calcula la nota total sumando puntajes de respuestas correctas.
        Actualiza nota_total, fecha_fin y estado.
        """
        total = 0
        for ra in self.respuestas.all():
            if ra.respuesta.es_correcta:
                total += ra.pregunta.puntaje

        self.nota_total = total
        self.estado = 'finalizado'
        self.fecha_fin = timezone.now()
        self.save()
        return self.nota_total

    def __str__(self):
        return f"{self.estudiante.nombre_completo} - {self.evaluacion.titulo}"


class RespuestaAlumno(models.Model):
    intento = models.ForeignKey(
        IntentoEvaluacion,
        on_delete=models.CASCADE,
        related_name='respuestas'
    )
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('intento', 'pregunta')

    def __str__(self):
        return f"{self.intento.estudiante.nombre_completo} - Pregunta {self.pregunta.id}"