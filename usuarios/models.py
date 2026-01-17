from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo debe ser proporcionado')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('rol', 'AdminC')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correo, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
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
    rol = models.CharField(max_length=30, choices=ROLES)
    estado = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['username', 'rol']

    class Meta:
        db_table = 'usuarios'

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
