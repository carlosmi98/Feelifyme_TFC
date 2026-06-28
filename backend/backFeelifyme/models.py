from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=100)
    apellido1 = models.CharField(max_length=100)
    apellido2 = models.CharField(max_length=100, blank=True, null=True)
    dni = models.CharField(
        max_length=100, 
        unique=True, 
        blank=True, 
        null=True
    )

    class Meta:
        ordering = ['nombre', 'apellido1']

    def __str__(self): 
        return f"{self.nombre} {self.apellido1} {self.apellido2 or ''}"

class Emocion(models.Model):
    class Nivel(models.TextChoices):
        Primario = "1", "Primario"
        Secundario = "2", "Secundario"
        Terciario = "3", "Terciario"

    nombre = models.CharField(
        max_length=100, 
        unique=True
    )
    nivel = models.CharField(
        max_length=1,
        choices=Nivel.choices
    )

    padre = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True, 
        related_name='hijas'
    )
    
    class Meta:
        ordering = ['nivel']
        verbose_name = "Emocion"
        verbose_name_plural = "Emociones"

    def __str__(self):
        return f"{self.nombre} ({self.get_nivel_display()})"

    _EMOCIONES_CACHE = None

    @classmethod
    def get_emociones_dict(cls) -> dict:
        """Devuelve el dict {id: {id, nombre, nivel, padre_id}} cargando desde
        la BD solo si todavía no está en caché."""
        if cls._EMOCIONES_CACHE is None:
            cls._EMOCIONES_CACHE = {
                e.id: {
                    "id": e.id,
                    "nombre": e.nombre,
                    "nivel": e.nivel,
                    "padre_id": e.padre_id,
                }
                for e in cls.objects.all()
            }
        return cls._EMOCIONES_CACHE

    @classmethod
    def get_emocion_primaria(cls, emocion_id: int, emociones_dict: dict = None) -> dict | None:
        """Sube por el árbol en memoria hasta encontrar la emoción de nivel '1'.
        Máximo 2 saltos (3→2→1). Devuelve {id, nombre} o None si no se encuentra."""
        if emociones_dict is None:
            emociones_dict = cls.get_emociones_dict()
        emocion = emociones_dict.get(emocion_id)
        while emocion and emocion["nivel"] != "1":
            emocion = emociones_dict.get(emocion["padre_id"])
        return emocion



class RegistroDiario(models.Model):
    usuario =models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name='registros'
    )
    fecha = models.DateField()
    notas = models.TextField(
        null=True, 
        blank=True,
        verbose_name="Nota diaria",
        help_text="Escribe una reflexión o suceso del día"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Registro diario"
        verbose_name_plural = "Registros diarios"
        
    def __str__(self): 
        return f"Registro de {self.usuario.username} - {self.fecha}"

class EmocionRegistrada(models.Model):
    registro = models.ForeignKey(
        RegistroDiario,
        on_delete=models.CASCADE,
        related_name='emociones_registradas'
    )

    emocion = models.ForeignKey(
        Emocion,
        on_delete=models.CASCADE,
        related_name='registros_asociados'
    )

    class Meta:
        unique_together = (('registro', 'emocion'),)
        verbose_name = "Emoción registrada"
        verbose_name_plural = "Emociones registradas"

    def __str__(self):
        return f"{self.emocion} → {self.registro.fecha}"

class Actividad(models.Model):
    nombre = models.CharField(
        max_length=100, 
        unique=True
    ) 
    #a futuro añadir mais actividades e clasificar
    # categoria = models.CharField()  model novo?

    class Meta: 
        ordering = ['nombre'] 

    def __str__(self): return self.nombre

class ActividadRealizada(models.Model):
    registro = models.ForeignKey(
        RegistroDiario,
        on_delete=models.CASCADE,
        related_name='actividades_realizadas'
    )

    actividad = models.ForeignKey(
        Actividad,
        on_delete=models.CASCADE,
        related_name='registros_asociados'
    )

    class Meta:
        unique_together = (('registro', 'actividad'),)
        verbose_name = "Actividad realizada"
        verbose_name_plural = "Actividades realizadas"

    def __str__(self):
        return f"{self.actividad.nombre} en registro {self.registro.id}"

class Logro(models.Model):
    nombre = models.CharField(
        max_length=100, 
        unique=True
    ) 
    descripcion = models.TextField() 
    tipo = models.CharField(
        max_length=50, 
        blank=True, 
        null=True
    )
    # a futuro? rankings para motivacion?
    # puntos = models.IntegerField(default=0)

    class Meta:
        ordering = ['nombre'] 
        verbose_name = "Logro"
        verbose_name_plural = "Logros"

    def __str__(self):
        return self.nombre

class LogroUsuario(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='logros_obtenidos'
    )
    logro = models.ForeignKey(
        Logro,
        on_delete=models.CASCADE,
        related_name='usuarios_que_lo_tienen'
    )
    fecha_obtenido = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = (('usuario', 'logro'),)
        ordering = ['usuario'] 
        verbose_name = "Logro usuario"
        verbose_name_plural = "Logros usuarios"
    def __str__(self): 
        return self.usuario.username

class Recomendacion(models.Model):
    titulo = models.CharField(
        max_length=100, 
        unique=True
    ) 
    descripcion = models.TextField() 
    emociones = models.ManyToManyField(
        Emocion,
        through="RecomendacionEmocion",
        related_name="recomendaciones"
    )
    def __str__(self): 
        return self.titulo

class RecomendacionEmocion(models.Model):
    recomendacion = models.ForeignKey(
        Recomendacion,
        on_delete=models.CASCADE,
        related_name='emociones_asociadas'
    )

    emocion = models.ForeignKey(
        Emocion,
        on_delete=models.CASCADE,
        related_name='recomendaciones_relacionadas'
    )

    class Meta:
        unique_together = (('recomendacion', 'emocion'),)
        ordering = ['recomendacion'] 
        verbose_name = "Relación recomendación-emoción"
        verbose_name_plural = "Relaciones recomendación-emoción"
    def __str__(self): 
        return f"{self.recomendacion} → {self.emocion}"