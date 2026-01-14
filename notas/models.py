from django.db import models
from usuarios.models import Usuario
from evaluaciones.models import Evaluacion

class Nota(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE,
                                   limit_choices_to={'rol': 'estudiante'},
                                   related_name='notas')
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='notas')
    nota_obtenida = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_realizado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('estudiante', 'evaluacion')
    
    def __str__(self):
        return f"{self.estudiante.username} - {self.evaluacion.titulo} - {self.nota_obtenida}"
