from django.db import models
from usuarios.models import Usuario

class Curso(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('borrador', 'Borrador')
    ]
    
    titulo = models.CharField(max_length=255)
    descripcion_breve = models.CharField(max_length=255, blank=True)
    descripcion = models.TextField(blank=True)
    imagen = models.CharField(max_length=255, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cupos = models.PositiveIntegerField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    profesor = models.ForeignKey(Usuario, on_delete=models.CASCADE,
                                 limit_choices_to={'rol': 'profesor'},
                                 related_name='cursos')
    
    def __str__(self):
        return self.titulo

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='modulos')
    titulo = models.CharField(max_length=255)
    orden = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['orden']
    
    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"
