from django.db import models
from cursos.models import Modulo

class Leccion(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=255)
    contenido = models.TextField(blank=True)
    orden = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['orden']
    
    def __str__(self):
        return f"{self.modulo.titulo} - {self.titulo}"

class RecursoLeccion(models.Model):
    TIPO_CHOICES = [
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('archivo', 'Archivo'),
        ('enlace', 'Enlace')
    ]
    
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, related_name='recursos')
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    archivo = models.FileField(upload_to='recursos/', blank=True, null=True)
    url_enlace = models.URLField(max_length=500, blank=True, null=True)  
    descripcion = models.CharField(max_length=255, blank=True)
    orden = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.leccion.titulo} - {self.tipo}"