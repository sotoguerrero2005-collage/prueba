from django.db import models
from django.contrib.auth.hashers import make_password

class Usuario(models.Model):
    ROLES = (
        ('AdminP', 'Administrador de Pagos'),
        ('AdminC', 'Administrador de Cursos'),
        ('profesor', 'Profesor'),
        ('estudiante', 'Estudiante'),
    )

    id_usuario = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    nombre_completo = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    cedula = models.CharField(max_length=50, unique=True, blank=True, null=True)
    rol = models.CharField(max_length=30, choices=ROLES)
    password = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios'

    def save(self, *args, **kwargs):
        # Guardar la contraseña en hash solo si hay un valor y no está hasheada
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_completo} ({self.rol})"


class UserActivity(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE) 
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_activity'

    def __str__(self):
        return f"{self.user.nombre_completo} - {self.action}"
