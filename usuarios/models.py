from django.db import models

class Usuario(models.Model):
    ROLES = (
        ('AdminP', 'Administrador de Pagos'),
        ('AdminC', 'Administrador de Cursos'),
        ('profesor', 'Profesor'),
        ('estudiante', 'Estudiante'),
    )
    
    id_usuario = models.BigAutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    cedula = models.CharField(max_length=50, unique=True, blank=True, null=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=50, choices=ROLES)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'usuarios'
        managed = False  # Django no intentará crear/modificar esta tabla
