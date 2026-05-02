"""
Modelos de datos para la aplicación 'deportes'.

Define la estructura de las disciplinas deportivas del club, sus
galerías de imágenes y la organización/resultados de los partidos.
"""

from django.db import models


class Disciplina(models.Model):
    """
    Representa una disciplina deportiva que se practica en el club.

    Attributes:
        nombre (CharField): Nombre oficial del deporte.
        slug (SlugField): URL amigable para acceso a la página.
        color_hex (CharField): Color de identidad visual para UI.
        imagen_portada (ImageField): Foto cabecera para la disciplina.
        descripcion (TextField): Texto libre con días, horarios o historia.
    """
    nombre = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    color_hex = models.CharField(
        max_length=7, 
        default='#2E7D32', 
        help_text="Color para las etiquetas (ej: #FF0000)"
    )

    imagen_portada = models.ImageField(upload_to='deportes/portadas/', null=True, blank=True)
    descripcion = models.TextField(blank=True, help_text="Información sobre la disciplina, horarios, etc.")

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"

    def __str__(self):
        return self.nombre


class ImagenDisciplina(models.Model):
    """
    Entidad para gestionar múltiples fotos asociadas a una única disciplina.

    Attributes:
        disciplina (ForeignKey): Relación a la disciplina a la que pertenece la foto.
        imagen (ImageField): Archivo físico subido.
        epigrafe (CharField): Texto opcional para describir la escena.
        orden (PositiveIntegerField): Entero para ordenar visualmente la grilla.
    """
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='imagenes')
    
    # El uso de %Y/%m/ (año/mes) previene que una sola carpeta en el servidor 
    # acumule miles de archivos y ralentice el sistema operativo al leerlos.
    imagen = models.ImageField(upload_to='deportes/galeria/%Y/%m/')
    epigrafe = models.CharField(max_length=200, blank=True)
    orden = models.PositiveIntegerField(default=0, help_text="Para ordenar las fotos en la galería.")

    class Meta:
        verbose_name = "Imagen de Galería"
        verbose_name_plural = "Imágenes de Galería"
        
        # Mantener un ordering por defecto simplifica las consultas (Queries) 
        # en las vistas frontend asegurando la presentación deseada.
        ordering = ['orden']

    def __str__(self):
        # Nota: Depender de un FK (self.disciplina.nombre) en __str__ requiere que 
        # las tablas y vistas usen select_related para evitar cuellos de botella "N+1".
        return f"Foto {self.id} de {self.disciplina.nombre}"


class Partido(models.Model):
    """
    Acontecimiento deportivo individual entre el club ('Arbolito') y un rival.

    Attributes:
        disciplina (ForeignKey): Deporte que se disputa.
        rival (CharField): Nombre de la institución contraria.
        fecha_hora (DateTimeField): Cuándo se juega.
        lugar (CharField): Sede del encuentro.
        es_local (BooleanField): Determina si se juega en casa.
        link_entradas (URLField): Enlace de redirección externa.
        activo (BooleanField): Si es False, el partido se oculta de listados públicos.
        resultado_arbolito (PositiveSmallIntegerField): Goles/puntos propios.
        resultado_rival (PositiveSmallIntegerField): Goles/puntos visitantes.
    """
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='partidos')
    rival = models.CharField(max_length=100)
    
    # Optimización crucial de la BD: Como 'fecha_hora' se usa por defecto 
    # para ordenar los resultados todo el tiempo en Meta, indexarlo acelera 
    # el motor SQL enormemente (un índice "B-Tree").
    fecha_hora = models.DateTimeField(db_index=True)
    
    lugar = models.CharField(max_length=200, default="Estadio Principal")
    es_local = models.BooleanField(default=True)
    link_entradas = models.URLField(blank=True, null=True, help_text="Opcional: Link a la ticketera")
    
    # Las consultas que omiten históricos suelen hacer `filter(activo=True)`.
    # Indexarlo contribuye a acelerar esos escaneos masivos.
    activo = models.BooleanField(default=True, db_index=True, help_text="Desmarcar para ocultar el partido")
    
    # Utilizar null=True permite distinguir limpiamente un resultado 
    # vacío ("El partido no ocurrió aún") de un "0" (Anotaron 0 goles).
    resultado_arbolito = models.PositiveSmallIntegerField(
        null=True, 
        blank=True, 
        help_text="Goles/Puntos de Arbolito. Dejar en blanco si aún no se jugó."
    )
    resultado_rival = models.PositiveSmallIntegerField(
        null=True, 
        blank=True, 
        help_text="Goles/Puntos del Rival. Dejar en blanco si aún no se jugó."
    )

    class Meta:
        verbose_name = "Partido"
        verbose_name_plural = "Partidos"
        ordering = ['fecha_hora']

    def __str__(self):
        prefijo = "vs" if self.es_local else "visitante contra"
        return f"{self.disciplina.nombre} {prefijo} {self.rival}"

    @property
    def ya_jugado(self):
        """
        DRY Extracción Lógica: Propiedad que evita repetir el "if resultado != None" 
        múltiples veces en el código. Expresa la intención de lectura en templates y vistas.
        """
        return self.resultado_arbolito is not None and self.resultado_rival is not None
