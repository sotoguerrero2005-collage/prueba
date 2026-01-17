# populate_db.py
import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from usuarios.models import Usuario
from cursos.models import Curso, Modulo
from lecciones.models import Leccion, RecursoLeccion
from inscripciones.models import Inscripcion
from evaluaciones.models import Evaluacion, Pregunta, Respuesta
from pagos.models import Pago

# -----------------------------
# Función para crear usuarios
# -----------------------------
def create_usuario(nombre, correo, rol, password, is_staff=False, is_superuser=False):
    user = Usuario.objects.create_user(
        correo=correo,
        password=password,
        username=correo.split("@")[0],
        nombre_completo=nombre,
        rol=rol,
        is_staff=is_staff,
        is_superuser=is_superuser
    )
    return user

# -----------------------------
# 1️⃣ Crear Usuarios
# -----------------------------
estudiante = create_usuario("Estudiante Uno", "estudiante@test.com", "estudiante", "pass123")
profesor = create_usuario("Profesor Uno", "profesor@test.com", "profesor", "pass123")
adminC = create_usuario("Admin Cursos", "adminC@test.com", "AdminC", "pass123", is_staff=True, is_superuser=True)
adminP = create_usuario("Admin Pagos", "adminP@test.com", "AdminP", "pass123", is_staff=True)

# -----------------------------
# 2️⃣ Crear Cursos
# -----------------------------
cursos = []
for i in range(1, 4):  # 3 cursos
    curso = Curso.objects.create(
        titulo=f"Curso {i}",
        descripcion_breve=f"Breve descripción del curso {i}",
        descripcion=f"Descripción detallada del curso {i}",
        profesor=profesor,
        estado="activo",
        precio=100 + i*10
    )
    cursos.append(curso)

# -----------------------------
# 3️⃣ Crear Módulos y Lecciones
# -----------------------------
for curso in cursos:
    for m in range(1, 3):  # 2 módulos por curso
        modulo = Modulo.objects.create(
            curso=curso,
            titulo=f"Módulo {m} de {curso.titulo}",
            orden=m
        )
        # 2 lecciones por módulo
        for l in range(1, 3):
            leccion = Leccion.objects.create(
                modulo=modulo,
                titulo=f"Lección {l} de {modulo.titulo}",
                orden=l
            )
            # Recursos: video y PDF
            RecursoLeccion.objects.create(
                leccion=leccion,
                tipo="video",
                url_enlace=f"https://videos.com/{curso.titulo}-{modulo.titulo}-{l}.mp4",
                orden=1
            )
            RecursoLeccion.objects.create(
                leccion=leccion,
                tipo="pdf",
                url_enlace=f"https://docs.com/{curso.titulo}-{modulo.titulo}-{l}.pdf",
                orden=2
            )

# -----------------------------
# 4️⃣ Crear Evaluaciones, Preguntas y Respuestas
# -----------------------------
for curso in cursos:
    evaluacion = Evaluacion.objects.create(
        curso=curso,
        titulo=f"Evaluación de {curso.titulo}",
        estado="activa"
    )
    for p in range(1, 3):  # 2 preguntas por evaluación
        pregunta = Pregunta.objects.create(
            evaluacion=evaluacion,
            texto=f"Pregunta {p} de {curso.titulo}"
        )
        for r in range(1, 3):  # 2 respuestas por pregunta
            Respuesta.objects.create(
                pregunta=pregunta,
                texto=f"Respuesta {r}",
                es_correcta=(r == 1)
            )

# -----------------------------
# 5️⃣ Inscribir solo al estudiante en un curso
# -----------------------------
curso_inscrito = cursos[0]  # solo el primer curso
inscripcion = Inscripcion.objects.create(
    estudiante=estudiante,
    curso=curso_inscrito,
    estado="activa"
)

# -----------------------------
# 6️⃣ Crear Pago para ese estudiante
# -----------------------------
Pago.objects.create(
    inscripcion=inscripcion,
    estudiante=estudiante,
    metodo_pago="transferencia",
    monto=curso_inscrito.precio,
    estado="aprobado"
)

print("Base de datos poblada correctamente.")
