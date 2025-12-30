import os
import django
from decimal import Decimal

# 1. Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from django.utils import timezone
# Importa tus modelos (ajusta el nombre de la app 'tu_app')
from usuarios.models import Usuario 
from cursos.models import Curso, Inscripcion, ContenidoCurso,  Pago, Nota, Respuesta, Evaluacion # Ajusta según tus apps

def populate():
    print("Iniciando carga de datos...")

    # --- 1. Crear Usuarios ---
    # Creamos un profesor
    profe, _ = Usuario.objects.get_or_create(
        correo="profe@escuela.com",
        defaults={
            'nombre_completo': 'Dr. Armando Backend',
            'password': make_password('profe123'),
            'rol': 'profesor',
            'estado': True
        }
    )

    # Creamos un estudiante
    alumno, _ = Usuario.objects.get_or_create(
        correo="estudiante@demo.com",
        defaults={
            'nombre_completo': 'Maria Estudiante',
            'password': make_password('alumno123'),
            'rol': 'estudiante',
            'estado': True
        }
    )

    # Creamos un Admin (para verificar pagos)
    admin_p, _ = Usuario.objects.get_or_create(
        correo="admin@pagos.com",
        defaults={
            'nombre_completo': 'Control Pagos',
            'password': make_password('admin123'),
            'rol': 'AdminP',
            'estado': True
        }
    )

    # --- 2. Crear Cursos ---
    curso_django, _ = Curso.objects.get_or_create(
        titulo="Master en Django & Angular",
        defaults={
            'descripcion_breve': 'Aprende a unir el mejor Backend con el mejor Frontend.',
            'descripcion': 'Curso completo de desarrollo web moderno.',
            'precio': Decimal('49.99'),
            'profesor': profe,
            'estado': 'activo'
        }
    )

    # --- 3. Crear Inscripción ---
    # Cambia 'id_alumno' por 'alumno' y 'id_curso' por 'curso'
    inscripcion, _ = Inscripcion.objects.get_or_create(
        alumno=alumno,       # La variable del modelo ahora es 'alumno'
        curso=curso_django,  # La variable del modelo ahora es 'curso'
        defaults={'estado': 'confirmado'}
    )

    # --- 4. Crear un Pago ---
    Pago.objects.get_or_create(
        inscripcion=inscripcion,  # Cambiado de id_inscripcion a inscripcion
        defaults={
            'metodo_pago': 'Transferencia',
            'referencia': 'REF123456',
            'monto': Decimal('49.99'),
            'estado': 'verificado',
            'verificado_por': admin_p, # Asegúrate de usar la variable del admin que creaste arriba
            'fecha_verificacion': timezone.now()
        }
    )

    print("¡Éxito! Datos creados correctamente.")
    print(f"Login Estudiante -> Correo: estudiante@demo.com | Pass: alumno123")

if __name__ == '__main__':
    populate()