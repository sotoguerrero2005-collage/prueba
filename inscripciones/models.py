from django.db import models
from usuarios.models import Usuario
from cursos.models import Curso

class Inscripcion(models.Model):

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('activa', 'Activa'),
        ('rechazada', 'Rechazada')
    ]
    
    estudiante = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'estudiante'},
        related_name='inscripciones'
    )
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('estudiante', 'curso')
    
    def __str__(self):
        return f"{self.estudiante.username} - {self.curso.titulo} ({self.estado})"
