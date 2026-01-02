from django.db import models
from usuarios.models import Usuario

class Curso(models.Model):
    id_curso = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion_breve = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.CharField(max_length=255, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Cambié el nombre de la variable a 'profesor'
    profesor = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, db_column='id_profesor')
    
    estado = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'cursos'
        managed = False

class Inscripcion(models.Model):
    id_inscripcion = models.BigAutoField(primary_key=True)
    # Cambié los nombres a 'alumno' y 'curso'
    alumno = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_alumno')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, db_column='id_curso')
    estado = models.CharField(max_length=50)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'inscripciones'
        managed = False

class ContenidoCurso(models.Model):
    id_contenido = models.BigAutoField(primary_key=True)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, db_column='id_curso')
    tipo = models.CharField(max_length=50) # Video, PDF, etc.
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    ruta_archivo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'contenido_curso'
        managed = False

class Evaluacion(models.Model):
    id_evaluacion = models.BigAutoField(primary_key=True)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, db_column='id_curso')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=50)

    class Meta:
        db_table = 'evaluaciones'
        managed = False

class Pregunta(models.Model):
    id_pregunta = models.BigAutoField(primary_key=True)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, db_column='id_evaluacion')
    pregunta_texto = models.TextField()

    class Meta:
        db_table = 'preguntas'
        managed = False

class Respuesta(models.Model):
    id_respuesta = models.BigAutoField(primary_key=True)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, db_column='id_pregunta')
    texto_respuesta = models.TextField()
    es_correcta = models.BooleanField()

    class Meta:
        db_table = 'respuestas'
        managed = False

class Pago(models.Model):
    id_pago = models.BigAutoField(primary_key=True)
    inscripcion = models.ForeignKey('Inscripcion', on_delete=models.CASCADE, db_column='id_inscripcion')
    metodo_pago = models.CharField(max_length=50)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    captura_comprobante = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=50)
    verificado_por = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, db_column='verificado_por', null=True)
    fecha_verificacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'pagos'
        managed = False

class Nota(models.Model):
    id_nota = models.BigAutoField(primary_key=True)
    alumno = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_alumno')
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, db_column='id_evaluacion')
    nota_obtenida = models.DecimalField(max_digits=5, decimal_places=2)
    aprobado = models.BooleanField()
    fecha_realizado = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notas'
        managed = False