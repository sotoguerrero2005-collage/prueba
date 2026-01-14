# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from usuarios.views import UsuarioViewSet, login
from cursos.views import CursoViewSet
from lecciones.views import LeccionViewSet
from inscripciones.views import InscripcionViewSet
from evaluaciones.views import EvaluacionViewSet, IntentoEvaluacionViewSet, RespuestaAlumnoViewSet
from pagos.views import PagoViewSet
from notas.views import NotaViewSet


router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'lecciones', LeccionViewSet)
router.register(r'inscripciones', InscripcionViewSet)
router.register(r'evaluaciones', EvaluacionViewSet)
router.register(r'pagos', PagoViewSet)
router.register(r'notas', NotaViewSet)
router.register(r'intentos', IntentoEvaluacionViewSet)
router.register(r'respuestas-alumno', RespuestaAlumnoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', login, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
