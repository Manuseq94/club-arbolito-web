"""
Configuración de la aplicación 'institucion' del proyecto Django.

Define parámetros transversales para todo el módulo encargado de
las noticias, el carrusel principal y las categorías deportivas/sociales.
"""

from django.apps import AppConfig


class InstitucionConfig(AppConfig):
    """
    Clase de inicialización para la aplicación 'institucion'.

    Attributes:
        default_auto_field (str): Tipo de campo autoincremental para las Primary Keys.
        name (str): Ruta principal de acceso al módulo (requerido por Django).
    """
    
    # Utilizar BigAutoField asegura un límite máximo de identificadores primarios (IDs)
    # virtualmente inagotable, previniendo caídas del sistema si las tablas de multimedia 
    # o noticias crecen a ritmos exponenciales en el transcurso de los años.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Se incluye el prefijo 'apps.' obedeciendo a un diseño de arquitectura limpia (Clean Architecture)
    # que agrupa las aplicaciones dentro de una subcarpeta, evitando ensuciar el directorio raíz del proyecto.
    name = 'apps.institucion'

