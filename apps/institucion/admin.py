"""
Configuración del panel de administración para la aplicación 'institucion'.

Define la visualización y permisos de gestión de Noticias, Categorías, 
Imágenes de Carrusel y Multimedia en el administrador de Django.
"""

from django.contrib import admin

from .models import Categoria, ImagenCarrusel, Multimedia, Noticia


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Configuración administrativa para las categorías de noticias.

    Attributes:
        list_display (tuple): Columnas a mostrar en el panel.
        prepopulated_fields (dict): Reglas de autocompletado en el formulario.
        search_fields (tuple): Campos sobre los que actuará la barra de búsqueda.
    """
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    """
    Configuración administrativa para la entidad Noticia.

    Attributes:
        list_display (tuple): Columnas principales incluyendo datos relacionales.
        list_filter (tuple): Criterios en el panel de filtro lateral izquierdo.
        search_fields (tuple): Campos de texto indizados para búsqueda interna.
        ordering (tuple): Orden descendente cronológico por defecto.
        list_editable (tuple): Campos de modificación directa o en lote.
        list_select_related (tuple): Relaciones a pedir vía JOIN para optimizar BD.
    """
    list_display = (
        'titulo', 'categoria', 'fecha_publicacion', 
        'es_destacada', 'activo'
    )
    list_filter = ('categoria', 'es_destacada', 'activo', 'fecha_publicacion')
    search_fields = ('titulo', 'bajada', 'cuerpo')
    ordering = ('-fecha_publicacion',)
    
    # Facilitar la administración permitiendo resaltar ("es_destacada") o dar de 
    # baja ("activo") noticias rápidamente sin necesidad de entrar a la edición de cada una.
    list_editable = ('es_destacada', 'activo')
    
    # Optimización: Cargar el ForeignKey `categoria` mediante SQL JOIN  
    # para evitar consultas redundantes (N+1) al renderizar la columna en list_display.
    list_select_related = ('categoria',)


@admin.register(ImagenCarrusel)
class ImagenCarruselAdmin(admin.ModelAdmin):
    """
    Configuración administrativa para el Carrusel publicitario o de anuncios.
    """
    list_display = ('titulo', 'orden', 'activo', 'imagen')
    list_editable = ('orden', 'activo')
    ordering = ('orden',)
    

@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    """
    Gestor de archivos de la galería o sector audiovisual.
    """
    list_display = ('descripcion', 'fecha_subida', 'tiene_imagen', 'tiene_video')
    
    # PEP 8 & Limpieza Moderna: Se utilizó el decorador nativo de Django '@admin.display'
    # el cual reemplaza la inyección anti-estética de asignaciones como `tiene_imagen.boolean = True`
    # ubicadas directamente en el root scope de la clase.
    @admin.display(boolean=True, description='Tiene Imagen')
    def tiene_imagen(self, obj):
        """Devuelve True si el registro posee al menos un archivo de imagen válido."""
        return bool(obj.imagen)

    @admin.display(boolean=True, description='Tiene Video')
    def tiene_video(self, obj):
        """Devuelve True si el registro posee al menos un archivo de video válido."""
        return bool(obj.video)
