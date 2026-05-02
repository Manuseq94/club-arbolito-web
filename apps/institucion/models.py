"""
Modelos de datos para la aplicación 'institucion'.

Gestiona las entidades centrales del club que no están estrictamente 
relacionadas al deporte, como su sistema de noticias, el carrusel principal
y una galería multimedia mixta (imágenes/videos).
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    """
    Clasificación temática que agrupa a las diferentes noticias.

    Attributes:
        nombre (CharField): Título de la categoría (ej: "Sociales").
        slug (SlugField): URL amigable única para SEO.
    """
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre


class Noticia(models.Model):
    """
    Representa una publicación o artículo periodístico del club.

    Attributes:
        titulo (CharField): Encabezado de la noticia.
        bajada (TextField): Breve resumen para el preview o tarjeta.
        cuerpo (TextField): Texto principal completo.
        imagen_portada (ImageField): Foto de presentación superior.
        categoria (ForeignKey): Relación "Muchos a Uno" con Categoría.
        es_destacada (BooleanField): Marca para ubicar la noticia en portada VIP.
        fecha_publicacion (DateTimeField): Momento cronológico del alta.
        activo (BooleanField): Soft-delete flag.
    """
    titulo = models.CharField(max_length=200)
    bajada = models.TextField(help_text="Resumen corto para la tarjeta de la página principal.")
    cuerpo = models.TextField(help_text="Contenido completo de la noticia.")
    imagen_portada = models.ImageField(upload_to='noticias/%Y/%m/', null=True, blank=True)
    
    # Se implementó models.PROTECT intencionalmente en este diseño arquitectónico. 
    # Impide que eliminar una categoría por accidente termine borrando en 
    # cascada (CASCADE) el historial histórico integral de noticias del club.
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='noticias')
    
    # Permite a los Editores clavar la publicación en el "Hero" de la página principal.
    es_destacada = models.BooleanField(
        default=False, 
        help_text="¿Mostrar en la columna central de novedades?"
    )
    
    fecha_publicacion = models.DateTimeField(default=timezone.now, db_index=True)
    
    # El indexado de `activo` acelera queries comunes del tipo `.filter(activo=True)`.
    activo = models.BooleanField(
        default=True, 
        db_index=True, 
        help_text="Permite ocultar la noticia sin borrarla de la base de datos (Soft Delete)."
    )

    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        # El orden cronológico invertido (del más nuevo al más viejo) es 
        # el estándar absoluto en sistemas de CMS de noticias.
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return self.titulo


class ImagenCarrusel(models.Model):
    """
    Slide visual individual que conforma el encabezado rotativo de la web.

    Attributes:
        titulo (CharField): Overlay opcional de texto sobre la foto.
        imagen (ImageField): Archivo de formato apaisado.
        orden (PositiveIntegerField): Entero definitorio de aparición.
        activo (BooleanField): Permite guardar banners estacionales apagados.
    """
    titulo = models.CharField(max_length=100, blank=True, help_text="Opcional. Texto que aparece sobre la imagen.")
    imagen = models.ImageField(
        upload_to='carrusel/',
        help_text='ATENCIÓN: Para que no se corte, subir fotos horizontales (apaisadas). Tamaño recomendado: 1920x1080 píxeles.'
    )
    orden = models.PositiveIntegerField(default=0, help_text="Para elegir qué foto aparece primero.")
    activo = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'Imagen de Carrusel'
        verbose_name_plural = 'Imágenes de Carrusel'
        ordering = ['orden']

    def __str__(self):
        # Evitamos concatenar `titulo` de forma directa sin comprobación, 
        # ya que es opcional y podría insertar basura vacía como "Carrusel 1 - ".
        ext = f" - {self.titulo}" if self.titulo else ""
        return f"Imagen Carrusel {self.id}{ext}"
    

class Multimedia(models.Model):
    """
    Registro unitario de álbum fotográfico o videoteca general de la institución.

    Acepta de manera mutuamente excluyente o bien una imagen, o bien un vídeo.

    Attributes:
        descripcion (CharField): Texto de ancla (caption).
        imagen (ImageField): Foto estándar.
        video (FileField): Clip multimedia bruto (ej. MP4).
        fecha_subida (DateTimeField): Timestamp automático de creación.
    """
    descripcion = models.CharField(max_length=250, help_text="Pie de foto o descripción del video")
    
    # Se dividieron las lógicas de subida a carpetas separadas (img/ vs vid/) 
    # para permitir futuras limpiezas limpias de servidor y evitar colisiones de mime-types.
    imagen = models.ImageField(upload_to='institucion/galeria/img/', null=True, blank=True, help_text="Subir foto (JPG/PNG)")
    video = models.FileField(upload_to='institucion/galeria/vid/', null=True, blank=True, help_text="Subir video (idealmente MP4 corto).")
    
    fecha_subida = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Item de Galería"
        verbose_name_plural = "Galería Multimedia"
        ordering = ['-fecha_subida']

    def clean(self):
        """
        DRY Extracción Lógica y Constraints: Mantiene la integridad de modelo asegurando 
        que el usuario no pueda subir simultáneamente imagen Y video al mismo componente.
        """
        super().clean()
        if self.imagen and self.video:
            raise ValidationError("No puedes subir una imagen y un video al mismo tiempo. Selecciona solo uno.")
        if not self.imagen and not self.video:
            raise ValidationError("Debes proveer al menos una imagen o un video.")

    def __str__(self):
        return f"{self.descripcion[:50]}..." if len(self.descripcion) > 50 else self.descripcion
